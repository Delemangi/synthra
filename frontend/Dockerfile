# Development stage
FROM --platform=${BUILDPLATFORM} node:20 AS development
WORKDIR /workspace/frontend

COPY package.json package-lock.json ./
RUN npm ci --ignore-scripts

COPY . ./
RUN npm run build

# Production stage
FROM --platform=${TARGETPLATFORM} node:20 AS production
WORKDIR /workspace/frontend

COPY --from=development /workspace/frontend .

RUN npm prune --production && npm i vite --ignore-scripts && npm cache clean --force

CMD [ "npm", "run", "preview" ]
