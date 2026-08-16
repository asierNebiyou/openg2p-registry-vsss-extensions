# Staff Portal UI — built from registry-platform ui/staff-portal-ui @ REPO_URL/GIT_BRANCH.
FROM node:20-alpine AS base
WORKDIR /app

FROM base AS builder

RUN apk add --no-cache git
ARG REPO_URL
ARG GIT_BRANCH
RUN git clone --branch "${GIT_BRANCH}" --depth 1 "${REPO_URL}" /src
WORKDIR /src/ui/staff-portal-ui

RUN npm ci
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM base AS runner

ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs \
    && adduser --system --uid 1001 nextjs

COPY --from=builder /src/ui/staff-portal-ui/public ./public
COPY --from=builder --chown=nextjs:nodejs /src/ui/staff-portal-ui/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /src/ui/staff-portal-ui/.next/static ./.next/static

RUN npm install sharp

RUN chown -R nextjs:nodejs /app
USER nextjs

EXPOSE 3000

CMD ["node", "server.js"]
