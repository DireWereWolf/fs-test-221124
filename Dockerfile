# Use the official PostgreSQL image from the Docker Hub
FROM postgres:latest

# Set environment variables (can be overridden via Docker Compose or `docker run`)
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=fstestpass
ENV POSTGRES_DB=fs_test_221124

# Expose the default PostgreSQL port
EXPOSE 5432