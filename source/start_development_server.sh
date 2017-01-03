#!/usr/bin/env bash
set -e
docker build -t test/event_handler .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/event_handler:/event_handler test/event_handler
