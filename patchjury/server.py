"""Local single-user app. Only explicit POST can spend credits or run fixtures."""
import json, pathlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from .fixtures import FIXTURES
from .provider import Budget, generate
from .runner import compare
ROOT=pathlib.Path(__file__).resolve().parent.parent/'web'
class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, type='application/json'):
        if not isinstance(body,bytes): body=json.dumps(body).encode()
        self.send_response(code); self.send_header('Content-Type',type); self.send_header('Content-Length',str(len(body))); self.send_header('X-Content-Type-Options','nosniff'); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path=='/api/fixtures':
            self.send(200,{k:{'title':v['title'],'spec':v['spec']} for k,v in FIXTURES.items()}); return
        if self.path=='/api/budget': self.send(200,Budget().status()); return
        files={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript'),'/style.css':('style.css','text/css')}
        if self.path not in files: self.send(404,{'error':'Not found'}); return
        filename,mime=files[self.path]; self.send(200,(ROOT/filename).read_bytes(),mime)
    def do_POST(self):
        # JSON + same origin + local Host prevents cross-site spending and DNS rebinding.
        host=self.headers.get('Host','')
        origin=self.headers.get('Origin')
        if host not in ['127.0.0.1:8000','localhost:8000'] or (origin and origin not in ['http://'+host]) or self.headers.get('Content-Type')!='application/json':
            self.send(403,{'error':'Local same-origin JSON required'}); return
        if self.path!='/api/compare': self.send(404,{'error':'Not found'}); return
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=1024: raise ValueError('Invalid request size')
            data=json.loads(self.rfile.read(length)); fixture=data.get('fixture'); mode=data.get('mode')
            if fixture not in FIXTURES or mode not in ['live','authored-example']: raise ValueError('Invalid fixture or mode')
            if mode=='live': cases,provenance=generate(fixture)
            else: cases,provenance=FIXTURES[fixture]['examples'],{'mode':mode,'model':None,'note':'Hand-authored, not recorded model output.'}
            self.send(200,compare(fixture,cases,provenance))
        except (ValueError,KeyError,json.JSONDecodeError) as e: self.send(400,{'error':str(e)})
        except Exception as e:
            self.log_error('%s',type(e).__name__)
            self.send(503,{'error':'Run failed. Check server logs, sandbox availability, and API configuration.'})
def serve():
    print('Patch Jury → http://127.0.0.1:8000',flush=True)
    HTTPServer(('127.0.0.1',8000),Handler).serve_forever()
