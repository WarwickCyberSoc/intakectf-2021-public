FROM node:16

# Create app directory
WORKDIR /usr/src/app

COPY ./app/package*.json ./

RUN npm ci --only=production

# Bundle app source
COPY ./app .

EXPOSE 3000
CMD [ "node", "index.js" ]