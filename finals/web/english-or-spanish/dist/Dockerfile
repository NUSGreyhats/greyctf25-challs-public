FROM node:20

WORKDIR /app

COPY . .

RUN echo "grey{REDACTED}" > flag

RUN useradd --create-home --shell /bin/bash user
RUN chmod -R +rx /app

RUN yarn install --no-cache

USER user
EXPOSE 3000

CMD ["yarn", "start"]
