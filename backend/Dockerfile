ARG PLATFORM="linux/amd64"

FROM --platform=${PLATFORM} python:3.11-alpine AS requirements
WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM --platform=${PLATFORM} python:3.11-alpine AS base
WORKDIR /code

RUN apk update && apk add --no-cache build-base && apk cache clean

COPY --from=requirements /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
