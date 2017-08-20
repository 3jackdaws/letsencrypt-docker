FROM    python:alpine

RUN     apk update && apk add certbot gcc musl-dev; \
        mkdir /app; \
        pip3 install docker-py; \
        apk del gcc



WORKDIR /app
ADD . .
ENV     EMAIL ""

VOLUME /keys
VOLUME /webroot
VOLUME /var/run/docker.sock
VOLUME /sites

ENTRYPOINT sh -c "python3 docker_events.py;sh"


