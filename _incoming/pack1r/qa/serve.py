#!/usr/bin/env python3
"""Read-only served-equivalent route map; no estate files are modified or copied."""
import json, mimetypes, urllib.request
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
POP=json.loads((ROOT/'qa/population.json').read_text())
routes={'/'+r['target']:ROOT/r['html'] for r in POP}
for r in POP:routes['/'+str(Path(r['target']).parent/'START_HERE.html')]=ROOT/'landing'/Path(r['target']).parent.name/'START_HERE.html'
routes['/index.html']=REPO/'index.html'
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  path=self.path.split('?')[0]
  try:
   if path=='/hud.js':
    with urllib.request.urlopen('https://madebymatt.uk/hud.js',timeout=25) as response:data=response.read()
    mime='text/javascript'
   else:
    file=routes.get(path)
    if file is None:
     candidate=(ROOT/path.lstrip('/')).resolve()
     if not candidate.is_relative_to(ROOT):raise FileNotFoundError(path)
     file=candidate
    data=file.read_bytes();mime=mimetypes.guess_type(str(file))[0] or 'application/octet-stream'
   self.send_response(200);self.send_header('Content-Type',mime+'; charset=utf-8' if mime.startswith(('text/','application/json')) else mime);self.end_headers();self.wfile.write(data)
  except Exception:self.send_error(404)
 def log_message(self,*args):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
