# Development stage
FROM --platform=${BUILDPLATFORM} python:3.11 AS development
WORKDIR /workspace/backend

COPY ./pyproject.toml ./poetry.lock ./
RUN pip install poetry

RUN poetry install && poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY . ./

# Production stage
FROM --platform=${TARGETPLATFORM} python:3.11 AS production
WORKDIR /workspace/backend

COPY --from=development /workspace/backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./app ./app

CMD [ "python", "-m", "app.main" ]
