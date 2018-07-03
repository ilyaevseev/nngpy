#!/bin/sh

cd "$(dirname "$0")"

export PYTHONPATH=..

python pubsub-server.py &
pid1=$!
sleep 2  # ..wait for listening

python pubsub-client.py &
pid2=$!

sleep 5  # ..do work

kill "$pid1" "$pid2"

## END ##
