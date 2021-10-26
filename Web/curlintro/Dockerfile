FROM node:15

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY ./app/package*.json ./

# If you are building your code for production
RUN npm ci --only=production

# Bundle app source
COPY ./app/ .

ENV PORT=8080
EXPOSE ${PORT}

ENV NODE_ENV=production

CMD [ "node", "index.js" ]