FROM node:19-buster

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app
COPY init.sh ./
CMD ["node", "mdServer.js"]