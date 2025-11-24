# -*- coding: utf-8 -*-
"""
WSGI config for the Café Application.

This module contains the WSGI callable as a module-level variable named ``application``.
"""

import os
from app import create_app, db
from app.models import *  # Import all your models here

# Create the Flask application instance using the configuration from environment
application = create_app(os.getenv('FLASK_ENV') or 'development')

# Ensure all models are loaded and database tables are created
with application.app_context():
    db.create_all()
    print("Database tables created/verified")

if __name__ == "__main__":
    # This is only used when running the application directly (not through a WSGI server)
    application.run()
