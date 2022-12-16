FROM node:19-buster

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install app
COPY mdServer.js /usr/src/app
EXPOSE 3000
CMD ["node", "mdServer.js"]