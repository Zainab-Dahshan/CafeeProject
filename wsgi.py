""
WSGI config for the Café Application.

This module contains the WSGI callable as a module-level variable named ``application``.
"""
import os
from app import create_app

# Create the Flask application instance using the production configuration
application = create_app('production')

if __name__ == "__main__":
    # This is only used when running the application directly (not through a WSGI server)
    application.run()
