#!/usr/bin/python

import nng

rep = nng.Reply()
rep.listen("ipc:///tmp/nngpy-repreq")
while True:
    s = rep.recv()
    rep.send("Received by server from client: " + s)

## END ##
