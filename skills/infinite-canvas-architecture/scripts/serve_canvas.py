"""Serve only generated atlas artifacts on IPv4 loopback."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import re
from pathlib import Path
from urllib.parse import unquote,urlsplit

def make_server(root,port=0):
    root=Path(root).resolve()
    manifest=json.loads((root/'canvas-manifest.json').read_text(encoding='utf-8'))
    if manifest.get('generator')!='infinite-canvas-architecture-v1':raise ValueError('Unrecognized canvas manifest')
    allowed=set(manifest['files'])
    if any(not isinstance(name,str) or not re.fullmatch(r'[A-Za-z0-9._-]+\.(html|json|svg)',name) for name in allowed):
        raise ValueError('Manifest must contain plain artifact filenames')
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):self.serve(False)
        def do_HEAD(self):self.serve(True)
        def serve(self,head):
            path=unquote(urlsplit(self.path).path)
            name='index.html' if path=='/' else path[1:]
            if name not in allowed:self.send_error(404);return
            target=(root/name).resolve()
            if target.parent!=root:self.send_error(404);return
            try:content=target.read_bytes()
            except OSError:self.send_error(404);return
            kind={'html':'text/html','json':'application/json','svg':'image/svg+xml'}[target.suffix[1:]]
            self.send_response(200);self.send_header('Content-Type',kind+'; charset=utf-8')
            self.send_header('Content-Length',str(len(content)));self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer')
            self.send_header('Content-Security-Policy',"default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data: blob:; connect-src 'none'; base-uri 'none'; form-action 'none'")
            self.end_headers()
            if not head:self.wfile.write(content)
        def log_message(self,*args):pass
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('directory',type=Path);parser.add_argument('--port',type=int,default=0)
    args=parser.parse_args()
    try:server=make_server(args.directory,args.port)
    except (ValueError,OSError) as error:parser.exit(1,f'ERROR: {error}\n')
    print(f'http://127.0.0.1:{server.server_port}/',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()
