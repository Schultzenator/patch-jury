import http.client, threading, unittest
from http.server import HTTPServer
from patchjury.server import Handler
class ServerTests(unittest.TestCase):
    def setUp(self):
        self.server=HTTPServer(('127.0.0.1',0),Handler)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
    def tearDown(self): self.server.shutdown();self.server.server_close();self.thread.join()
    def req(self,method,path,body=None,headers=None):
        c=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=3)
        c.request(method,path,body,headers or {});r=c.getresponse();data=r.read();c.close();return r.status,data
    def test_static_types_and_no_traversal(self):
        for path in ['/','/app.js','/style.css','/api/fixtures']:
            self.assertEqual(self.req('GET',path)[0],200)
        self.assertEqual(self.req('GET','/../TASK.md')[0],404)
    def test_cross_origin_rebinding_and_get_cannot_spend(self):
        self.assertEqual(self.req('GET','/api/compare')[0],404)
        for headers in [{'Host':'evil.example','Content-Type':'application/json'}, {'Host':'localhost:8000','Origin':'https://evil.example','Content-Type':'application/json'},{'Host':'localhost:8000','Content-Type':'text/plain'}]:
            self.assertEqual(self.req('POST','/api/compare','{}',headers)[0],403)
    def test_invalid_data(self):
        self.assertEqual(self.req('POST','/api/compare','{"fixture":"../../etc/passwd","mode":"live"}',{'Host':'localhost:8000','Content-Type':'application/json'})[0],400)
