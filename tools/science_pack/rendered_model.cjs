/* The embedded no-video model must remain visible and render without video.
 * Image encoding is not the property: keep the existing img load assertion,
 * and require an inline SVG to decode and paint pixels with local references.
 */
'use strict';
const assert=require('node:assert/strict');
async function assertRenderedModel(figure){
  const model=figure.locator('img,svg');
  assert.equal(await model.count(),1,'Exactly one embedded no-video model is present');
  await model.scrollIntoViewIfNeeded();
  assert.equal(await model.isVisible(),true,'Embedded no-video model is visible');
  const status=await model.evaluate(async n=>{
    if(n.tagName.toLowerCase()==='img')return {ok:n.complete&&n.naturalWidth>0,kind:'img'};
    if(n.namespaceURI!=='http://www.w3.org/2000/svg')return {ok:false,reason:'Not an SVG'};
    const nodes=[n,...n.querySelectorAll('*')];
    const copy=n.cloneNode(true),copied=[copy,...copy.querySelectorAll('*')];
    // Preserve the actual page's inherited paint and visibility when rasterising.
    const properties=['display','visibility','opacity','fill','fill-opacity','stroke','stroke-opacity','stroke-width','font-family','font-size','font-weight','clip-path','mask','filter','marker-start','marker-mid','marker-end'];
    for(let i=0;i<nodes.length;i++){
      const style=getComputedStyle(nodes[i]);
      for(const property of properties)copied[i].style.setProperty(property,style.getPropertyValue(property));
    }
    const ids=new Set(copied.map(el=>el.id).filter(Boolean));
    // Computed styles can expand a local gradient/marker to a same-document
    // absolute URL. Validate its target inside this SVG, then keep it local
    // when serialising; an external document or absent ID is still a failure.
    const documentUrl=new URL(document.URL);documentUrl.hash='';
    const localReference=ref=>{
      let id;
      if(ref.startsWith('#'))id=decodeURIComponent(ref.slice(1));
      else{
        const target=new URL(ref,n.baseURI);id=decodeURIComponent(target.hash.slice(1));target.hash='';
        if(target.href!==documentUrl.href)throw new Error('External SVG reference: '+ref);
      }
      if(!id||!ids.has(id))throw new Error('Unresolved SVG reference: '+ref);
      return '#'+encodeURIComponent(id);
    };
    try{
      for(const el of copied)for(const attr of [...el.attributes]){
        let value=attr.value.replace(/url\(\s*['"]?([^)'"\s]+)['"]?\s*\)/g,(_,ref)=>'url("'+localReference(ref)+'")');
        if(attr.localName==='href')value=localReference(value);
        if(value!==attr.value)el.setAttributeNS(attr.namespaceURI,attr.name,value);
      }
    }catch(e){return {ok:false,reason:e.message};}
    const rect=n.getBoundingClientRect();
    copy.setAttribute('xmlns','http://www.w3.org/2000/svg');
    copy.setAttribute('width',String(Math.ceil(rect.width)));
    copy.setAttribute('height',String(Math.ceil(rect.height)));
    const image=new Image();
    image.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(new XMLSerializer().serializeToString(copy));
    try{
      await image.decode();
      const canvas=document.createElement('canvas');canvas.width=image.naturalWidth;canvas.height=image.naturalHeight;
      const ctx=canvas.getContext('2d');ctx.drawImage(image,0,0);
      const pixels=ctx.getImageData(0,0,canvas.width,canvas.height).data;
      for(let i=3;i<pixels.length;i+=4)if(pixels[i]>0)return {ok:true,kind:'svg'};
      return {ok:false,reason:'SVG decoded but paints no pixels'};
    }catch(e){return {ok:false,reason:'SVG fails to decode or render: '+e.message};}
  });
  assert.equal(status.ok,true,'Embedded no-video model loads and renders: '+JSON.stringify(status));
  return status;
}
module.exports={assertRenderedModel};
