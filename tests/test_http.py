import unittest,threading,json,urllib.request,urllib.error
from http.server import ThreadingHTTPServer
from cableroute.server import Handler
from cableroute.cli import load_case
class Http(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.url='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_assets(self):
        for path in ['/','/app.js','/style.css','/api/examples']:
            with urllib.request.urlopen(self.url+path) as response:self.assertEqual(response.status,200)
    def test_roundtrip(self):
        payload=json.dumps({'network':load_case('example:industrial')}).encode();request=urllib.request.Request(self.url+'/api/study',payload,{'Content-Type':'application/json'})
        with urllib.request.urlopen(request) as response:self.assertIn('provenance',json.load(response))
    def test_origin(self):
        request=urllib.request.Request(self.url+'/api/study',b'{}',{'Content-Type':'application/json','Origin':'http://evil.invalid'})
        with self.assertRaises(urllib.error.HTTPError) as caught:urllib.request.urlopen(request)
        self.assertEqual(caught.exception.code,403)
