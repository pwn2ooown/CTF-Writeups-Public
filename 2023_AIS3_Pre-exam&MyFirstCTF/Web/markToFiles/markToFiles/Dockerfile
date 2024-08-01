FROM node

# Create app directory
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . .

RUN npm install && echo "AIS3{fake}" > /flag

EXPOSE 3001

CMD [ "node", "app.js" ]