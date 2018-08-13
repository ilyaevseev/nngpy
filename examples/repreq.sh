#!/bin/sh

cd "$(dirname "$0")"

export PYTHONPATH=..

python3 repreq-server.py &
pid1=$!
sleep 2  # ..wait for listening

python3 repreq-client.py aa bb cc dd

kill "$pid1"

## END ##
