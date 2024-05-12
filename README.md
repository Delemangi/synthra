# Synthra

Synthra is a file hosting application built using [FastAPI](https://github.com/tiangolo/fastapi) (with Python 3.11) and [SvelteKit](https://github.com/sveltejs/kit), with PostgreSQL.

This repository contains both the frontend and the backend of the project in their respective folders.

## Features

- File hosting
- User registration & login
- Webhooks support

## Installation

For running the application in production mode, it's highly recommended to use Docker. Otherwise, the manual setup is also available for those who wish to test the application in a development environment.

### Quick Deployment

For most users, just these few steps should be sufficient, provided that you are comfortable with using Docker for deploying applications.

1. Grab the `docker-compose.prod.yaml` file from the repository
2. Rename it to `docker-compose.yaml`
3. Run `docker compose up -d`

### Development

To setup your environment and the project for development:

1. Run `poetry install` (while inside the `backend` folder)
2. Run `pre-commit install`

### Installation (Docker Setup)

The project contains two Docker Compose configurations. `docker-compose.yaml` is for the development environment, and `docker-compose.prod.yaml` is for the production environment.

1. Run `git clone git@github.com:Delemangi/synthra.git` (or `git clone https://github.com/Delemangi/synthra.git`)
2. Run `docker compose build`
   - If you need the Docker image built for a machine running ARM architecture, then use the `PLATFORM` build argument as such: `docker compose build --build-arg PLATFORM=linux/arm64`

### Installation (Manual Setup)

The manual setup requires that you have the following requirements installed:

- [Python](https://www.python.org/) >= v3.11
- [Poetry](https://python-poetry.org/)
- [Node.js](https://nodejs.org/en) >= v20
- [PostgreSQL](https://www.postgresql.org/) >= v16

Once you have all these dependencies installed, then:

1. Run `git clone git@github.com:Delemangi/synthra.git` (or `git clone https://github.com/Delemangi/synthra.git`)
2. Next, you have to install each module separately.

#### Backend

1. Navigate to the `backend` folder: `cd backend`
2. Run `poetry install`

#### Frontend

1. Navigate to the `frontend` folder: `cd frontend`
2. Run `npm i`
3. Run `npm run build`

## Running

### Running (Docker Setup)

1. Copy or rename the `.env.sample` file to `.env`, and edit it to your liking, or leave it as is
2. Run `docker compose up`

### Running (Manual Setup)

1. Start the PostgreSQL service
2. Start the backend service
   1. Open the project in your terminal
   2. Run `cd backend`
   3. Run `poetry run uvicorn app.main:app --host 0.0.0.0 --port 80 [--reload]` - the last parameter is optional, in case you want hot reloading
3. Start the frontend service
   1. Open the project in your terminal
   2. Run `cd frontend`
   3. If you would like to start the application in a development environment with hot reloading, then run `npm run dev`, otherwise `npm run preview`, provided that you have run `npm run build` previously
