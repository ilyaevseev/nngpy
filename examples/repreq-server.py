#!/usr/bin/python

import nng

rep = nng.Reply()
rep.listen("ipc:///tmp/nngpy-repreq")
while True:
    s = rep.recvstr()
    rep.sendstr("Received by server from client: " + s)

## END ##
