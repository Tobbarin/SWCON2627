"""Campus Circle, built through feature-first AI iterations. Python 3.12+."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class App(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/style.css':
            content = (ROOT / 'style.css').read_bytes()
            kind = 'text/css'
        elif self.path == '/':
            content = (ROOT / 'index.html').read_bytes()
            kind = 'text/html'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', kind + '; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), App)
    print(f'Campus Circle: http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
