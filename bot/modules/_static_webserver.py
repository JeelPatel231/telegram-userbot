from functools import partial
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import os

PORT = os.environ.get("PORT", 8000)

def runnable(_):
    handler = partial(SimpleHTTPRequestHandler, directory="pastes")
    httpd = TCPServer(("", PORT), handler)
    print("serving at port ", PORT)
    httpd.serve_forever()