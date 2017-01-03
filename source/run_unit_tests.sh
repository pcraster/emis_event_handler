#!/usr/bin/env bash
set -e


docker build -t test/event_handler .
docker run --env ENV=TEST -p5000:5000 test/event_handler
