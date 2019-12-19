# Send commands from command line to a WSL service that will execute them
# if they are registered.
import socket
import sys
import re

def replaceDrive( mo ):
    return "/mnt/{}/".format( mo.group(1).lower() )

HOST, PORT = "localhost", 9999
args = [ re.sub( r"^([a-z]):/", replaceDrive, s.replace( "\\", "/" ), count=1, flags=re.I )
        for s in sys.argv[1:] ]
args = [ '%s' % re.escape(s) for s in args ]
data = ("gvimsrv " + (" ".join(args))).encode( "utf-8" )

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + b"\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

