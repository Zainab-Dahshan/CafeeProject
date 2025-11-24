from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class BaseModel(db.Model):
    """Base model that includes common columns and methods."""
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Save the current model to the database."""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Delete the current model from the database."""
        db.session.delete(self)
        db.session.commit()
        return self
    
    def update(self, **kwargs):
        """Update the current model with the given attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

# Import all models to ensure they are registered with SQLAlchemy
from .user import User
from .menu_item import MenuItem
from .order import Order, OrderItem
