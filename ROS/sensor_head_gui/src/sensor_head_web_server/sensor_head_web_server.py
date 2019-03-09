#!/usr/bin/env python

import SimpleHTTPServer
import BaseHTTPServer
import SocketServer
import os
import ssl
import rospy


rospy.init_node(name="sensor_head_web_server_node_name", anonymous=True)

PORT = 4443
if rospy.has_param('~web_server_port'):
    PORT = rospy.get_param('~web_server_port')
else:
    PORT = 4443
    rospy.logwarn(
        "No parameter for web_server_port on the parameter server. Using port %s instead", PORT)


web_server_www_root = os.path.join(os.path.dirname(__file__), 'www')
if rospy.has_param('~web_server_www_root'):
    web_server_www_root = os.path.join(rospy.get_param('~web_server_www_root'))
else:
    web_server_www_root = os.path.join(os.path.dirname(__file__), 'www')
    rospy.logwarn(
        "No parameter for web_server_www_root on the parameter server. Using '%s' instead", web_server_www_root)

os.chdir(web_server_www_root)


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

httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                               certfile=os.path.expanduser("~")+'/s4e4gro.pem')


def shutdown_hook():
    print "Trying to shut down server"
    rospy.loginfo("Trying to shut down server")
    httpd.socket.close()


rospy.on_shutdown(shutdown_hook)

rospy.loginfo('Current web directory: %s', os.getcwd())
rospy.loginfo('Serving at port %s', PORT)

while not rospy.is_shutdown():
    httpd.serve_forever()
    rospy.spin()
    pass


# You can now open a browser to "https://localhost:4443" or replace localhost
# with the host's IP adress, or the computer's name if the full names are
# resolved. Adding the https is important.
