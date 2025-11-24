"""
Gunicorn configuration file for the Café Application.

This file contains production-ready configuration for Gunicorn.
"""

import multiprocessing
import os

# Server socket
bind = '0.0.0.0:5000'  # Listen on all network interfaces
backlog = 2048  # Maximum number of pending connections

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal worker count
worker_class = 'gevent'  # Using gevent for async workers
worker_connections = 1000  # Maximum number of simultaneous clients per worker
timeout = 30  # Worker timeout in seconds
keepalive = 2  # Seconds to keep connections alive

# Logging
loglevel = 'info'  # Log level
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log errors to stderr
access_log_format = '%(h)s %(l)s %(u)s; %(t)s; "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'  # Log format

# Process naming
proc_name = 'cafe_app'  # Process name

# Security
# Preload the application before forking worker processes
preload_app = True

# Maximum number of requests a worker will process before restarting
max_requests = 1000
max_requests_jitter = 50  # Random jitter to prevent all workers restarting at once

# Timeout for graceful shutdown
timeout = 120  # seconds
graceful_timeout = 30  # seconds

# Environment variables
raw_env = [
    'FLASK_APP=wsgi.py',
    'FLASK_ENV=production'
]
