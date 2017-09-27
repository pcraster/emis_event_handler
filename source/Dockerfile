FROM pcraster/emis_base:1.0.0

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY cmd.sh server.py /
COPY emis_event_handler /emis_event_handler
COPY test /test

CMD ["/cmd.sh"]
