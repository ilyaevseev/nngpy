#!/bin/sh

cd "$(dirname "$0")"

export PYTHONPATH=..

python repreq-server.py &
pid1=$!
sleep 2  # ..wait for listening

python repreq-client.py aa bb cc dd

kill "$pid1"

## END ##
