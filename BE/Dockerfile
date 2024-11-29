# Stage 1: Build environment
FROM python:3.13-alpine AS builder

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set a working directory
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    gcc \
    musl-dev \
    curl \
    make \
    openssl-dev \
    bash \
    && curl -sSLO https://github.com/vishnubob/wait-for-it/releases/download/v2.5.0/wait-for-it-linux-amd64 \
    && chmod +x wait-for-it-linux-amd64 \
    && mv wait-for-it-linux-amd64 /usr/local/bin/wait-for-it

# Copy requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Production environment
FROM python:3.13-alpine AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/app"

# Set a working directory
WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache \
    libffi \
    postgresql-libs \
    curl \
    openssl \
    bash

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . /app/

# Expose the port on which FastAPI will run
EXPOSE 9001

# Copy the start.sh script into the container and make it executable
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Use the script as the entry point
ENTRYPOINT ["/app/start.sh"]
