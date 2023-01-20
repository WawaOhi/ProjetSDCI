FROM ubuntu:trusty

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


# Install all the elements needed 
RUN apt-get update -y\
    && apt-get upgrade -y\
    && apt-get install curl -y\
    && apt-get install jq -y
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | apt-key add -
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install nodejs -yq\
    && npm init -y\ 
    && npm install express \
    && npm install systeminformation \
    && npm install yargs\
    && npm install request

# Install app
COPY ./init.sh  /usr/src/app
ENTRYPOINT ["/bin/bash", "init.sh"]
