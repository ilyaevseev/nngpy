#!/usr/bin/python

from datetime import datetime
import time
import nng

pub = nng.Publisher()
pub.listen("ipc:///tmp/nngpy-pubsub")

while True:
    t = datetime.now()
    f = t.strftime('%Y-%m-%d %H:%M:%S')
    pub.send("Sent by server: " + f)
    time.sleep(1)

## END ##
