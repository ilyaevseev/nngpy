#!/usr/bin/python

import sys
import nng

req = nng.Request()
req.connect("ipc:///tmp/nngpy-repreq")
for s in sys.argv:
    req.sendstr(s)
    print("Received by client from server: " + req.recvstr())

## END ##
