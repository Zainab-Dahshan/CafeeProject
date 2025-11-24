# Import db from base first to avoid circular imports
from .base import db

# Import models
# Note: These imports are done in app/__init__.py after the app is created
# to avoid circular imports

def init_app(app):
    """Initialize models with the Flask app."""
    # Import models here to avoid circular imports
    from .user import User
    from .menu_item import MenuItem
    from .order import Order, OrderItem
    
    # Make models available for import from app.models
    return {
        'User': User,
        'MenuItem': MenuItem,
        'Order': Order,
        'OrderItem': OrderItem,
        'db': db
    }

# This will be populated when init_app is called
User = MenuItem = Order = OrderItem = None
