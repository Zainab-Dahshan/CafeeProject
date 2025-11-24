from .base import db, BaseModel
from sqlalchemy import CheckConstraint

class MenuItem(BaseModel):
    """Menu item model for the café's menu."""
    __tablename__ = 'menu_items'
    
    # Basic information
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Item details
    category = db.Column(db.String(50), index=True)  # e.g., 'Coffee', 'Food', 'Dessert'
    is_available = db.Column(db.Boolean, default=True, index=True)
    is_featured = db.Column(db.Boolean, default=False, index=True)
    
    # Nutritional information (optional)
    calories = db.Column(db.Integer)
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    is_gluten_free = db.Column(db.Boolean, default=False)
    
    # Image and display
    image_url = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default=0)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='menu_item', lazy='dynamic')
    
    # Constraints
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
    )
    
    def __repr__(self):
        return f'<MenuItem {self.name} - ${self.price:.2f}>'
    
    def to_dict(self):
        """Convert the menu item to a dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0.0,
            'category': self.category,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'calories': self.calories,
            'dietary_info': {
                'vegetarian': self.is_vegetarian,
                'vegan': self.is_vegan,
                'gluten_free': self.is_gluten_free
            },
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_available_items(cls, category=None, featured_only=False):
        """Get available menu items, optionally filtered by category and featured status."""
        query = cls.query.filter_by(is_available=True)
        
        if category:
            query = query.filter_by(category=category)
            
        if featured_only:
            query = query.filter_by(is_featured=True)
            
        return query.order_by(cls.display_order, cls.name).all()
    
    @classmethod
    def get_categories(cls):
        """Get all unique menu categories."""
        return [row[0] for row in cls.query.with_entities(cls.category).distinct().all() if row[0]]
