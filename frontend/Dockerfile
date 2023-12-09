ARG PLATFORM="linux/amd64"

FROM --platform=${PLATFORM} node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm i

COPY src ./src
COPY static ./static

COPY tsconfig.json ./
COPY svelte.config.js ./
COPY vite.config.ts ./

RUN npm run build
RUN npm prune --production

FROM --platform=${PLATFORM} node:20-alpine AS release
WORKDIR /app

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/.svelte-kit ./.svelte-kit
COPY --from=build /app/static ./static
COPY --from=build /app/package.json ./

RUN npm i vite

CMD ["npm", "run", "preview"]
