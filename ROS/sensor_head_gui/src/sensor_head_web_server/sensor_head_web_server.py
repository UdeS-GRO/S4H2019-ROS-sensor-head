#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer
import os

PORT = 8000

web_dir = os.path.join(os.path.dirname(__file__), 'www')
os.chdir(web_dir)

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Current web directory serving", os.getcwd()
print "Serving at port", PORT
httpd.serve_forever()
