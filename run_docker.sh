#!/bin/bash

# Docker image and container names
IMAGE_NAME="my-flask-app"
CONTAINER_NAME="my-flask-app-container"

# Default environment is development if not specified
ENVIRONMENT=${1:-development}

# Load .env file if it exists
if [ -f ".env" ]; then
    echo ".env file found, loading environment variables..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️  WARNING: No .env file found! Ensure required variables are set manually."
fi

# Determine the correct Dockerfile and port mappings
if [ "$ENVIRONMENT" = "production" ]; then
    DOCKERFILE="Dockerfile.prod"
    PORT_MAPPING="${GUNICORN_PORT:-8000}:8000"
else
    DOCKERFILE="Dockerfile.dev"
    PORT_MAPPING="${FLASK_RUN_PORT:-5000}:5000"
fi

# Function to remove an existing container
remove_container() {
    if [ "$(docker ps -a -q -f name=^${CONTAINER_NAME}$)" ]; then
        echo "🚀 Stopping and removing existing Docker container..."
        docker stop ${CONTAINER_NAME}
        docker rm ${CONTAINER_NAME}
    fi
}

# Function to remove an existing image
remove_image() {
    if [ "$(docker images -q ${IMAGE_NAME})" ]; then
        echo "🗑 Removing existing Docker image..."
        docker rmi ${IMAGE_NAME}
    fi
}

# Cleanup previous instances
remove_container
remove_image

# Build the Docker image
echo "🔨 Building Docker image ($ENVIRONMENT mode)..."
docker build -t ${IMAGE_NAME} -f ${DOCKERFILE} .

# Start the container with proper environment settings
echo "🚀 Running the backend in ${ENVIRONMENT} mode..."
docker run --env-file .env -p ${PORT_MAPPING} --name ${CONTAINER_NAME} ${IMAGE_NAME}

echo "✅ Backend is now running on http://localhost:${PORT_MAPPING%:*}"
