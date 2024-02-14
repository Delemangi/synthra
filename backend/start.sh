#!/bin/bash

echo "Waiting for the database to be available..."
until PGPASSWORD="$POSTGRES_PASSWORD" pg_isready --host="$POSTGRES_HOST" --port="$POSTGRES_PORT" --username="$POSTGRES_USER" --dbname="$POSTGRES_DB"; do
  sleep 1
done

echo "Starting..."

if [ -z "$1" ]; then
  uvicorn app.main:app --host "0.0.0.0" --port 80
else
  poetry run uvicorn app.main:app --host "0.0.0.0" --port 80 --reload
fi
