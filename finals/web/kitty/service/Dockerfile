FROM node:alpine

RUN mkdir /app
COPY package.json /app
COPY package-lock.json /app
WORKDIR /app
RUN npm ci
RUN mkdir -p /secret
RUN mkdir -p /app/sandbox

COPY . . 
RUN mv /app/flag.txt /secret/flag-$(cat /app/flag.txt | base64 -w0)

EXPOSE 3334

CMD ["node", "app.js"]