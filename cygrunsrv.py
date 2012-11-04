# #!/bin/bython
import os, sys, time
import shlex
import SocketServer
import subprocess as subp

reqid = 0
apps = {
        "gvim":    (0, ["/home/mmarko/usr/bin/vim.gtk", "-g"]),
        "gvimsrv": (1, ["/home/mmarko/usr/bin/vim.gtk", "-g", "--servername", "CYGVIM", "--remote-silent"])
       }
def readRc():
    rcfile = "~/.config/cygrun/cygrunsrvrc"
    if not os.path.exists(rcfile):
        return
    f = open(rcfile)
    for line in f:
        if line.strip().startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3: continue
        apps[parts[0]] = ( int(parts[1]), + parts[2:] )

# B: get data by simulating stream-reads
class MyTCPStreamHandler(SocketServer.StreamRequestHandler):

    def writeln(self, message):
        tms = time.strftime("%H:%M:%S", time.localtime())
        sys.stdout.write("(%03d) %s: %s\n" % (reqid, tms, message));

    def handle(self):
        global reqid
        reqid += 1
        sys.stdout.write("----------\n")
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.writeln("Request from: %s" % self.client_address[0])
        self.data = self.rfile.readline().strip()
        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        if self.client_address[0] == '127.0.0.1' and len(self.data) > 0:
            self.runthis(self.data)
        else:
            self.writeln("Rejected.")
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

    def runthis(self, cmd):
        acmd = shlex.split(cmd)
        cid = acmd[0]
        #print acmd
        #for a in acmd: print "  ", a
        self.writeln("Command: %s" % cid)
        didrun = False
        if cid in apps:
            nargs = apps[cid][0]
            run = apps[cid][1]
            if len(acmd)-1 >= nargs:
                run = run + acmd[1:]
                try:
                    subp.Popen(run)
                    didrun = True
                except Exception as e:
                    print e
        if not didrun:
            self.writeln("Rejected.")


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    #server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server = SocketServer.TCPServer((HOST, PORT), MyTCPStreamHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        print "Waiting for your commands."
        server.serve_forever()
    except KeyboardInterrupt:
        print "Ctrl-C: We're done."

# vim: set fileencoding=utf-8 sw=4 sts=4 ts=8 et :vim
