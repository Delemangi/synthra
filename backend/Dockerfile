ARG PLATFORM="linux/amd64"

# Development stage
FROM python:3.11-alpine AS development
WORKDIR /workspace/backend

RUN apk add --no-cache postgresql-client git openjdk17 nodejs

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock ./

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN poetry install

COPY . ./

CMD ["sh", "./start.sh", "reload"]

# Production stage
FROM --platform=${PLATFORM} python:3.11-alpine AS production
WORKDIR /workspace/backend

RUN apk add --no-cache postgresql-client build-base

COPY ./start.sh ./start.sh

COPY --from=development /workspace/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /workspace/backend/requirements.txt

COPY ./app /workspace/backend/app

CMD ["sh", "./start.sh"]
