#!/usr/bin/env bash
set -e


docker build -t test/emis_event_handler .
docker run \
    --env EMIS_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/emis_event_handler:/emis_event_handler \
    test/emis_event_handler
