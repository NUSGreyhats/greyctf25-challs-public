FROM node:20

WORKDIR /app

COPY . .

RUN echo "grey{why_ju5t_why_j5_1mp0rts}" > flag

RUN useradd --create-home --shell /bin/bash user
RUN chmod -R +rx /app

RUN yarn install --no-cache

USER user
EXPOSE 3000

CMD ["yarn", "start"]
