FROM node:alpine
WORKDIR /app
COPY . .
RUN yarn
EXPOSE 4000
CMD ["node", "build/index.min.js"]