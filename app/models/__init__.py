# Import db and BaseModel from base first to avoid circular imports
from .base import db, BaseModel

# Import models
# Note: These imports are done here to ensure they are registered with SQLAlchemy
from .user import User
from .menu_item import MenuItem
from .order import Order, OrderItem

def init_app():
    """Initialize models with the Flask app.
    
    Returns:
        dict: A dictionary of model classes for easy access.
    """
    # This function is kept for backward compatibility
    # All models are already imported above
    return {
        'User': User,
        'MenuItem': MenuItem,
        'Order': Order,
        'OrderItem': OrderItem,
        'db': db
    }

# This will be populated when init_app is called
User = MenuItem = Order = OrderItem = None
