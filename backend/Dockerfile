# First stage: Build dependencies
FROM python:3.10-alpine AS requirements
WORKDIR /tmp
RUN apk update && apk upgrade
RUN apk add --no-cache pkgconfig \
                       gcc \
                       openldap \
                       libcurl \
                       python3-dev \
                       gpgme-dev \
                       libc-dev \
                       postgresql-dev \
    && rm -rf /var/cache/apk/*

RUN pip install poetry

COPY ./pyproject.toml /tmp/
COPY ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Second stage: Final image
FROM python:3.10-alpine AS base
WORKDIR /code

RUN apk update && apk upgrade
RUN apk add --no-cache pkgconfig \
                       gcc \
                       openldap \
                       libcurl \
                       python3-dev \
                       gpgme-dev \
                       libc-dev \
                       postgresql-dev \
    && rm -rf /var/cache/apk/*

# Copying the compiled dependencies from the first stage
COPY --from=requirements /tmp/requirements.txt /code/requirements.txt

# Installing runtime dependencies
RUN apk add --no-cache libffi

RUN pip install cython

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install uvicorn

COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
