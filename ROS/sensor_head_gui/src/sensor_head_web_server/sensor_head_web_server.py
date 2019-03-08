#!/usr/bin/env python

import SimpleHTTPServer, BaseHTTPServer
import SocketServer
import os
import ssl


PORT = 4443

web_dir = os.path.join(os.path.dirname(__file__), 'www')
os.chdir(web_dir)

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

# Create a SSL certificate by filling out the answers to the informations asked 
# by the program, and make sure to use the exact name (address) that will be
# used at the FQDN or YOUR name question:
#
# cd ~ && openssl req -new -x509 -keyout yourpemfile.pem -out yourpemfile.pem -days 365 -nodes
# 
# cd ~ && openssl req -new -x509 -keyout s4e4gro.pem -out s4e4gro.pem -days 365 -nodes
#
# Using a https connection is required to use the orientation and motion
# javascript interfaces, or else they do not work, since it was deprecated. The 
# certificate file is not included in the source control.

httpd.socket = ssl.wrap_socket (httpd.socket, server_side=True,
                                certfile=os.path.expanduser("~")+'/s4e4gro.pem')



print "Current web directory serving", os.getcwd()
print "Serving at port", PORT
httpd.serve_forever()

# You can now open a browser to "https://localhost:4443" or replace localhost 
# with the host's IP adress, or the computer's name if the full names are 
# resolved. Adding the https is important.
