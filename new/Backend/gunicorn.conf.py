# gunicorn.conf.py - Production WSGI configuration

import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', '5001')}"
backlog = 2048

# Worker processes
workers = int(os.environ.get('WEB_CONCURRENCY', 4))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help limit memory leaks
max_requests = 1000
max_requests_jitter = 100

# Log to stdout so logs are captured by Render
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "bank_portal_backend"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in future)
# keyfile = None
# certfile = None

# Performance tuning
preload_app = True
enable_stdio_inheritance = True