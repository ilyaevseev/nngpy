#!/usr/bin/python

import nng

sub = nng.Subscriber()
sub.subscribe()
sub.connect("ipc:///tmp/nngpy-pubsub")

while True:
    print("Received by client: " + sub.recv())

## END ##
