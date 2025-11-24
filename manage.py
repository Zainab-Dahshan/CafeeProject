#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""
import os
from app import create_app, db
from app.models.user import User
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem
from flask_migrate import Migrate, upgrade, migrate, init, stamp

# Create the application instance
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# Make shell context available
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'MenuItem': MenuItem,
        'Order': Order,
        'OrderItem': OrderItem
    }

# CLI commands
@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # Migrate database to latest revision
    upgrade()
    
    # Create default admin user if it doesn't exist
    admin_email = app.config.get('ADMIN_EMAIL', 'admin@cafewebsite.com')
    if not User.query.filter_by(email=admin_email).first():
        admin = User(
            username='admin',
            email=admin_email,
            first_name='Admin',
            is_admin=True
        )
        admin.password = os.getenv('ADMIN_PASSWORD', 'admin123')
        db.session.add(admin)
        db.session.commit()
        print('Created default admin user')
    
    # Add sample menu items if none exist
    if not MenuItem.query.first():
        from datetime import datetime
        sample_items = [
            {
                'name': 'Cappuccino',
                'description': 'Espresso with steamed milk and foam',
                'price': 3.50,
                'category': 'Coffee',
                'is_available': True,
                'is_featured': True,
                'calories': 120,
                'is_vegetarian': True,
                'is_vegan': False,
                'is_gluten_free': True
            },
            {
                'name': 'Latte',
                'description': 'Espresso with steamed milk',
                'price': 3.00,
                'category': 'Coffee',
                'is_available': True,
                'is_featured': True,
                'calories': 100,
                'is_vegetarian': True,
                'is_vegan': False,
                'is_gluten_free': True
            },
            {
                'name': 'Blueberry Muffin',
                'description': 'Freshly baked blueberry muffin',
                'price': 2.75,
                'category': 'Bakery',
                'is_available': True,
                'is_featured': True,
                'calories': 350,
                'is_vegetarian': True,
                'is_vegan': False,
                'is_gluten_free': False
            }
        ]
        
        for item_data in sample_items:
            item = MenuItem(**item_data)
            db.session.add(item)
        
        db.session.commit()
        print('Added sample menu items')

if __name__ == '__main__':
    app.cli()