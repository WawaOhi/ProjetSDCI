#FROM ubuntu:xenial
#MAINTAINER manuel.peuster@uni-paderborn.de
#
#RUN	apt-get update && apt-get install -y \
#	net-tools \
#        iputils-ping \
#	iproute
#
## set entry point for emulator gatekeeper
#ENV VIM_EMU_CMD "echo 'Hello World!'"
#ENV VIM_EMU_CMD_STOP "echo 'Stopping the container now.'"
#
## CMD should always point to /bin/bash to not block the emulator
#CMD /bin/bash

FROM python:3.7-slim-buster
COPY monitoring.py app/
WORKDIR /app

RUN	apt-get update && apt-get install -y \
	net-tools \
    iputils-ping \
	iproute
RUN pip install Flask APScheduler requests
EXPOSE 5000
ENTRYPOINT ["python3", "monitoring.py"]