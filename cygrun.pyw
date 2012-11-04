#!/bin/python
# Author: Marko Mahnič
# Created: October 2012
# License: GPL
import sys, re
import socket

HOST, PORT = "localhost", 9999
# args = [ s.replace("\\", "/") for s in sys.argv[1:] ]
args = [ '%s' % re.escape(s) for s in sys.argv[1:] ]
data = " ".join(args)

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # print "sending", args
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

#print "Sent:     {}".format(data)
#print "Received: {}".format(received)
# vim: set fileencoding=utf-8 sw=4 sts=4 ts=8 et :vim
