#!/usr/bin/env bash
# build.sh - Render deployment build script

set -o errexit  # exit on error

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create logs directory if it doesn't exist
mkdir -p logs

# Run any database migrations if needed
python -c "
import os
os.environ.setdefault('FLASK_ENV', 'production')
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created/updated successfully!')
"

echo "Build completed successfully!"