FROM    python:alpine

RUN     apk update && apk add certbot gcc musl-dev; \
        mkdir /app; \
        pip3 install watchdog ruamel.yaml; \
        apk del gcc



WORKDIR /app
ADD . .
ENV     DOMAIN ""
ENV     SUBDOMAINS ""
ENV     EMAIL ""
ENV     WEBROOT /webroot
ENV     SUBDOMAINS_ONLY=false

VOLUME /keys
VOLUME /webroot

ENTRYPOINT sh -c "python3 le_watch.py;sh"


