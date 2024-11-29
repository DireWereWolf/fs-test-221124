#!/bin/bash

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL to be ready..."
wait-for-it postgres:5432 --timeout=30 --strict -- echo "PostgreSQL is up!"

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
python ./src/main.py
