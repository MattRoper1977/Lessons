// Run from a machine with Playwright Chromium installed. This exports HTML directly.
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require('playwright');
const root=path.resolve(process.argv[2]||'.');
async function walk(dir){const found=[];for(const e of await fs.readdir(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())found.push(...await walk(p));else found.push(p)}return found}
const files=(await walk(root)).filter(p=>/_(Pupil_Resources|Knowledge_Organiser|Word_Page)\.html$/.test(p));
const browser=await chromium.launch({headless:true});
const evidence=[];
try{
 for(const file of files){
  const page=await browser.newPage({viewport:{width:1280,height:800}});
  await page.goto(pathToFileURL(file).href,{waitUntil:'load'});
  await page.emulateMedia({media:'print'});
  await page.evaluate(()=>document.fonts.ready);
  const title=await page.title();
  const output=file.replace(/\.html$/,'.pdf');
  await page.pdf({path:output,format:'A4',preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false});
  evidence.push({html:path.relative(root,file),pdf:path.relative(root,output),title,renderer:await browser.version()});
  await page.close();
 }
}finally{await browser.close()}
await fs.writeFile(path.join(root,'chromium_export_evidence.json'),JSON.stringify(evidence,null,2));
console.log(`Exported ${evidence.length} pupil PDFs. Apply metadata with finalize_pdf_metadata.py and regenerate SHA256SUMS before delivery.`);
