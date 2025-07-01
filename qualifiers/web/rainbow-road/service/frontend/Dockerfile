FROM node:slim AS builder
WORKDIR /app
COPY . .
RUN yarn
RUN yarn build

# ─────────────── Stage 2: Nginx + copy in build artifacts ───────────────
FROM nginx:alpine
# copy over built static files
COPY --from=builder /app/dist  /usr/share/nginx/html
# drop in your custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf