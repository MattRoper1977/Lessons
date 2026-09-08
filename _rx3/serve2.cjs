// Two-root static server: /Lessons/* -> LESSONS root, everything else -> SITE root. Usage: node serve2.cjs <lessonsRoot> <siteRoot> <port>
const http=require('http'),fs=require('fs'),path=require('path');
const [lessons,site,port]=process.argv.slice(2);
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript','.css':'text/css','.json':'application/json','.webp':'image/webp','.png':'image/png','.svg':'image/svg+xml','.mp4':'video/mp4','.woff2':'font/woff2'};
http.createServer((req,res)=>{let u=decodeURIComponent(req.url.split('?')[0]);let root=site;if(u.startsWith('/Lessons/')){root=lessons;u=u.slice(8);}
let p=path.join(root,u);if(p.endsWith('/'))p+='index.html';fs.readFile(p,(e,d)=>{if(e){res.writeHead(404);res.end('404');return;}res.writeHead(200,{'content-type':types[path.extname(p)]||'application/octet-stream'});res.end(d);});}).listen(+port,'127.0.0.1',()=>console.log('serve2 on',port));
