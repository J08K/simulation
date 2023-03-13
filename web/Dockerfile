FROM node:19-alpine3.17 AS deps

RUN apk add --no-cache libc6-compat
WORKDIR /web

COPY package.json package-lock.json ./
RUN npm install --production

FROM node:19-alpine3.17 AS builder
WORKDIR /web

COPY --from=deps /web/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED 1

RUN npm run build

FROM node:19-alpine3.17 AS runner
WORKDIR /web

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder --chown=nextjs:nextjs /web/.next ./.next
COPY --from=builder /web/node_modules ./node_modules
COPY --from=builder /web/package.json ./package.json

USER nextjs

EXPOSE 3000

ENV PORT 3000

RUN ls

CMD ["npm", "start"]