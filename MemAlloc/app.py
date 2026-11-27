"""Local web server. Run with Python 3.10+; no third-party packages required."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from algorithms import compare

STATIC = Path(__file__).resolve().parent / 'static'


class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, status, content, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status, payload):
        self.send_bytes(status, json.dumps(payload).encode(), 'application/json; charset=utf-8')

    def do_GET(self):
        files = {'/': ('index.html', 'text/html'), '/style.css': ('style.css', 'text/css'),
                 '/script.js': ('script.js', 'application/javascript')}
        if self.path not in files:
            self.send_json(404, {'error': 'Not found'})
            return
        name, content_type = files[self.path]
        self.send_bytes(200, (STATIC / name).read_bytes(), content_type + '; charset=utf-8')

    def do_POST(self):
        if self.path != '/api/simulate':
            self.send_json(404, {'error': 'Not found'})
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 16000:
                raise ValueError('Invalid request size.')
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError('Invalid request.')
            result = compare(payload.get('blocks'), payload.get('processes'), payload.get('mode', 'dynamic'))
            self.send_json(200, {'results': result})
        except (ValueError, TypeError) as exc:
            self.send_json(400, {'error': str(exc)})


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 8501), Handler)
    print('MemAlloc is running at http://127.0.0.1:8501 (Ctrl+C to stop)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
