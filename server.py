from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import ssl
import os

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        path = path + '/airplane.png'
        print("Path: ", path)
        if path.startswith('images/'):
            print("1st level")
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

httpd = HTTPServer(('localhost', 4443), MyRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile="key.pem", 
        certfile='cert.pem', server_side=True)

httpd.serve_forever()