from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import threading
import random
import sys
import os

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        if path.startswith('images/'):
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            path = path + '/' + self.randomTLSContent()
            print("Path: ", path)
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        elif path.startswith('stego/'):
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            path = path + '/' + self.getStegoContent()
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        elif path.startswith('messages/'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            path = path + '/' + self.getMessageContent()
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def getMessageContent(self):
        files = os.listdir("messages/")
        random_integer = random.randint(0, len(files)-1)
        subString = "msg" + str(random_integer) + "."
        for fileName in files:
            if subString in fileName:
                subString = subString  + fileName[-3:]
        fileName = subString
        print("message file: ", subString)
        return fileName

    # Serve content randomly from the images dir
    def randomTLSContent(self):
        content = ["airplane.png", "arctichare.png", "baboon.png", "trailer.jpg", "watch.png"]
        random_integer = random.randint(0, len(content)-1)
        return content[random_integer]
    
    def getStegoContent(self):
        files = os.listdir("stego/")
        random_integer = random.randint(0, len(files)-1)
        subString = "stego" + str(random_integer) + "."
        for fileName in files:
            if subString in fileName:
                subString = subString  + fileName[-3:]
        fileName = subString
        print("Stego file: ", subString)
        return fileName


def stop_server():
    httpd.shutdown()

try:
    httpd = HTTPServer(('localhost', 80), MyRequestHandler)

    t = threading.Timer(310.0, stop_server)
    t.start()

    httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopping server...")
    httpd.shutdown()
    httpd.server_close()
    sys.exit(0)