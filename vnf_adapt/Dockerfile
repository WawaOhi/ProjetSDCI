FROM node:alpine

RUN mkdir /code
WORKDIR /code
ADD . /code

RUN apk update \
    && npm install url \
    && npm install http-forward

ENTRYPOINT node /code/load_balancer.js ; tail -f /dev/null

