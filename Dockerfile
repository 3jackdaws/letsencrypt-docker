FROM    python:alpine

RUN     apk update && apk add certbot gcc musl-dev; \
        mkdir /app; \
        pip3 install watchdog ruamel.yaml; \
        apk del gcc



WORKDIR /app
ADD . .
ENV     DOMAIN      example.com
ENV     SUBDOMAINS  "www,ww3,sub"
ENV     LE_EMAIL    "exmp@example.com"

VOLUME /config
VOLUME /etc/letsencrypt/live

ENTRYPOINT sh -c "python3 le_watch.py;sh"


