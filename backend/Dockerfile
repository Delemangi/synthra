ARG PLATFORM="linux/amd64"

# Development stage
FROM python:3.11-alpine AS development
WORKDIR /synthra

RUN apk add --no-cache postgresql-client git openjdk17 nodejs

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /synthra/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

# Production stage
FROM --platform=${PLATFORM} python:3.11-alpine AS production
WORKDIR /synthra

RUN apk add --no-cache postgresql-client build-base

COPY ./start.sh /synthra/start.sh

COPY --from=development /synthra/requirements.txt /synthra/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /synthra/requirements.txt

COPY ./app /synthra/app

CMD ["sh", "./start.sh"]
