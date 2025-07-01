FROM node:22-alpine AS base

FROM base AS builder
WORKDIR /app
RUN corepack enable pnpm

COPY \
    next.config.ts \
    package.json \
    pnpm-lock.yaml \
    tsconfig.json \
    ./
RUN pnpm i --frozen-lockfile

COPY app/ ./app/

RUN pnpm run build

FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000

ENV HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
