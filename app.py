#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import requests
import re

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if None != re.search('/api/red/*', self.path):
            self._set_response()
            r = requests.get(url='http://red')
            self.wfile.write(json.dumps(r.json()).encode(encoding='utf_8'))
            return
        if None != re.search('/api/blue/*', self.path):
            self._set_response()
            r = requests.get(url='http://blue')
            self.wfile.write(json.dumps(r.json()).encode(encoding='utf_8'))
            return
        else:
            self._set_response()
            self.wfile.write(json.dumps({'name': 'front','version': '1'}).encode(encoding='utf_8'))
            return

# HTTP Server runs on port 8080 
def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting server...\n')

    # start listening 
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()