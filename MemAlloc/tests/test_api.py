import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from app import Handler


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def post(self, payload):
        req = Request(self.base+'/api/simulate', data=json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
        with urlopen(req, timeout=5) as r:
            return json.load(r)

    def test_static_files(self):
        for path, token in [('/', b'MemAlloc'), ('/style.css', b'.metrics'), ('/script.js', b'/api/simulate')]:
            with urlopen(self.base+path, timeout=5) as r:
                self.assertEqual(r.status, 200)
                self.assertIn(token, r.read())

    def test_compare(self):
        result = self.post({'blocks':[100,500,200,300,600], 'processes':[212,417,112,426]})
        self.assertEqual([r['allocated'] for r in result['results']], [3,4,3])

    def test_invalid(self):
        with self.assertRaises(HTTPError) as exc:
            self.post({'blocks':[0], 'processes':[1]})
        self.assertEqual(exc.exception.code, 400)
        exc.exception.close()

    def test_fixed(self):
        result = self.post({'blocks':[100], 'processes':[40,60], 'mode':'fixed'})
        self.assertEqual([r['internal'] for r in result['results']], [60,60,60])
