#!/usr/bin/env bash
# Frontend build script for Render deployment

set -o errexit  # exit on error

echo "Installing dependencies..."
npm ci

echo "Running type checks..."
npm run lint

echo "Building the application..."
npm run build

echo "Frontend build completed successfully!"
echo "Static files are ready in the 'out' directory"