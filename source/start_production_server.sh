#!/usr/bin/env bash
set -e


docker build -t test/event_handler .
docker run -p3031:3031 test/event_handler
