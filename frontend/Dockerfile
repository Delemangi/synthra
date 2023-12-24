ARG PLATFORM="linux/amd64"

# Development stage
FROM node:20-alpine AS development
WORKDIR /workspace/frontend

RUN apk add --no-cache postgresql-client git openjdk17 nodejs

COPY package.json package-lock.json ./
RUN npm i

COPY . ./

CMD ["npm", "run", "dev"]

# Production stage
FROM --platform=${PLATFORM} node:20-alpine AS production
WORKDIR /workspace/frontend

RUN apk add --no-cache postgresql-client

COPY package.json ./
COPY --from=development /workspace/frontend/node_modules ./node_modules
RUN npm prune --production && npm i --ignore-scripts vite

COPY . ./
RUN npm run build

CMD ["npm", "run", "preview"]
