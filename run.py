#!/usr/bin/env python3
"""
Main entry point for the application.
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem

# Create the application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """
    Make shell context available in the Flask shell.
    """
    return {
        'db': db,
        'User': User,
        'MenuItem': MenuItem,
        'Order': Order,
        'OrderItem': OrderItem
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
