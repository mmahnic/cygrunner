# Python 3
#
# Open files from Windows File System in an instance of GVim running on a WSL2
# system.
#
# - Input parameters are treated as files and are modified.
# - DISPLAY environment variable is calculated from the /etc/resolv.conf file
#   on the Linux system (the firlst nameserver setting is used).
# - GVim is executed through WSL.
#
import os, sys, re
import subprocess as subp

def replaceDrive( mo ):
    return "/mnt/{}/".format( mo.group(1).lower() )

args = [ re.sub( r"^([a-z]):/", replaceDrive, s.replace( "\\", "/" ), count=1, flags=re.I )
        for s in sys.argv[1:]
        if not s.startswith("-") ]
args = [ '%s' % re.escape(s) for s in args ]

nameserver_ip = subp.check_output( ["wsl", "bash", "-c",
    "cat /etc/resolv.conf | grep nameserver" ] ).decode( "utf-8" )
mo = re.search( r"\d+\.\d+\.\d+\.\d+", nameserver_ip )
if mo is None:
    ip = "localhost"
else:
    ip = mo.group()

os.environ["DISPLAYIP"] = ip # debugging
os.environ["DISPLAY"] = "{}:0".format( ip )
os.environ["WSLENV"] = "DISPLAY:DISPLAYIP"
subp.call( ["wsl", "gvim", "--servername", "GVIM", "--remote-silent" ] + args )
