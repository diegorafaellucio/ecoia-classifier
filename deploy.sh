#!/bin/bash

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_NAME="ecoia-classifier"
PORT="8000"
PYTHON_CMD="python3.11"
PIP_CMD="pip3.11"

# Check if a tag was provided
if [ $# -eq 1 ]; then
    TAG=$1
    echo "Deploying version: ${TAG}"
    
    # Checkout the specified tag
    git fetch --all --tags
    git checkout tags/${TAG}
else
    echo "No tag specified. Using current branch."
fi

# Upgrade pip and basic tools
${PIP_CMD} install --upgrade pip setuptools wheel --break-system-packages

# Install requirements
echo "Installing requirements..."
${PIP_CMD} install -r "${PROJECT_DIR}/requeriments_base.txt" --break-system-packages
${PIP_CMD} install -r "${PROJECT_DIR}/requeriments_torch.txt" --break-system-packages
${PIP_CMD} install -r "${PROJECT_DIR}/requeriments_ultralytics.txt" --break-system-packages

# Check if PM2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "PM2 is not installed. Please install PM2 first."
    echo "You can install it using: npm install pm2 -g"
    exit 1
fi

# Check if the app is already running in PM2
if pm2 list | grep -q "${APP_NAME}"; then
    echo "Stopping existing PM2 process..."
    pm2 stop "${APP_NAME}"
    pm2 delete "${APP_NAME}"
fi

# Start the application with PM2
echo "Starting application with PM2..."
pm2 start "${PROJECT_DIR}/manage.py" \
    --name "${APP_NAME}" \
    --interpreter "${PYTHON_CMD}" \
    -- runserver 0.0.0.0:${PORT}

echo "Deployment completed successfully!"
echo "The application is running at http://0.0.0.0:${PORT}"
echo "To check the status, run: pm2 status"
echo "To view logs, run: pm2 logs ${APP_NAME}"
