# syntax=docker/dockerfile:1
FROM node:22-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
COPY apps/web/package.json ./apps/web/package.json
COPY apps/web/package-lock.json* ./apps/web/
RUN npm install --workspace=apps/web --install-scripts

FROM node:22-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/apps/web/node_modules ./apps/web/node_modules
COPY . .
RUN npm run build --workspace=apps/web

FROM node:22-alpine AS runner
WORKDIR /app/apps/web
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=builder /app/apps/web/.next ./.next
COPY --from=builder /app/apps/web/public ./public
COPY --from=builder /app/apps/web/package.json ./package.json
COPY --from=builder /app/apps/web/node_modules ./node_modules
EXPOSE 3000
ENV PORT=3000
CMD ["npx", "next", "start"]
