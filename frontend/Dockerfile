# Build stage
FROM --platform=${BUILDPLATFORM} node:21 AS build
WORKDIR /workspace/frontend

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

ENV VITE_BASE_URL=https://synthra-backend.delemangi.com

COPY . ./
RUN npm run build

# Production stage
FROM --platform=${TARGETPLATFORM} node:21 AS production
WORKDIR /workspace/frontend

COPY package.json package-lock.json ./

COPY --from=build /workspace/frontend/build ./build

CMD [ "node", "build/index.js" ]
