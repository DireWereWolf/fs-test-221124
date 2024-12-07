# Define variables for services and images
POSTGRES_IMAGE = postgres
NG_IMAGE = fs_test_221124_ng
MONOLITH_IMAGE = fs_test_221124_monolith

# Build all the docker images
build: build_postgres build_ng build_monolith

# Build PostgreSQL image from Dockerfile
build_postgres:
	docker build -t $(POSTGRES_IMAGE) . --no-cache

# Build the Angular application image
build_ng:
	docker build -t $(NG_IMAGE) ./FE --no-cache

# Build the Monolith application image
build_monolith:
	docker build -t $(MONOLITH_IMAGE) ./BE --no-cache

# Start all services with Docker Compose
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs for all containers
logs:
	docker-compose logs -f

# Clean up all containers and images
clean:
	docker-compose down --volumes --rmi all

# Rebuild images and restart services
rebuild:
	make clean
	make build
	make up
