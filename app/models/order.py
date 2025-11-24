from datetime import datetime
from .base import db, BaseModel
from sqlalchemy import CheckConstraint

class Order(BaseModel):
    """Order model for customer orders."""
    __tablename__ = 'orders'
    
    # Order information
    order_number = db.Column(db.String(20), unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Status tracking
    status = db.Column(db.String(20), default='pending', index=True)  # pending, confirmed, preparing, ready, completed, cancelled
    
    # Customer information (denormalized for historical accuracy)
    customer_name = db.Column(db.String(120))
    customer_email = db.Column(db.String(120))
    customer_phone = db.Column(db.String(20))
    
    # Order details
    subtotal = db.Column(db.Numeric(10, 2), default=0.00)
    tax = db.Column(db.Numeric(10, 2), default=0.00)
    total = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Payment information
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid, refunded, etc.
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    
    # Delivery/Takeout
    order_type = db.Column(db.String(20), default='dine_in')  # dine_in, takeout, delivery
    table_number = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    order_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    confirmed_at = db.Column(db.DateTime)
    prepared_at = db.Column(db.DateTime)
    ready_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    # Constraints
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled')", 
                       name='check_order_status'),
        CheckConstraint("payment_status IN ('unpaid', 'paid', 'refunded', 'partially_refunded', 'failed')", 
                       name='check_payment_status'),
        CheckConstraint("order_type IN ('dine_in', 'takeout', 'delivery')", 
                       name='check_order_type'),
    )
    
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.generate_order_number()
    
    def generate_order_number(self):
        """Generate a unique order number."""
        if not self.order_number:
            # Format: YYMMDD + 4 random digits
            from random import randint
            date_part = datetime.utcnow().strftime('%y%m%d')
            random_part = f"{randint(1000, 9999)}"
            self.order_number = f"ORD-{date_part}-{random_part}"
    
    def calculate_totals(self):
        """Calculate order subtotal, tax, and total."""
        self.subtotal = sum(item.total_price for item in self.items)
        # Assuming a fixed tax rate of 8%
        self.tax = round(float(self.subtotal) * 0.08, 2)
        self.total = round(float(self.subtotal) + float(self.tax), 2)
    
    def update_status(self, new_status, commit=True):
        """Update the order status and set the corresponding timestamp."""
        self.status = new_status
        now = datetime.utcnow()
        
        if new_status == 'confirmed':
            self.confirmed_at = now
        elif new_status == 'preparing':
            self.prepared_at = now
        elif new_status == 'ready':
            self.ready_at = now
        elif new_status == 'completed':
            self.completed_at = now
        elif new_status == 'cancelled':
            self.cancelled_at = now
        
        if commit:
            db.session.commit()
    
    def to_dict(self):
        """Convert the order to a dictionary."""
        return {
            'id': self.id,
            'order_number': self.order_number,
            'status': self.status,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'subtotal': float(self.subtotal) if self.subtotal else 0.0,
            'tax': float(self.tax) if self.tax else 0.0,
            'total': float(self.total) if self.total else 0.0,
            'order_type': self.order_type,
            'table_number': self.table_number,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_orders_by_status(cls, status=None, user_id=None):
        """Get orders filtered by status and/or user ID."""
        query = cls.query
        
        if status:
            query = query.filter_by(status=status)
            
        if user_id:
            query = query.filter_by(user_id=user_id)
            
        return query.order_by(cls.order_date.desc()).all()


class OrderItem(BaseModel):
    """Order item model for items in an order."""
    __tablename__ = 'order_items'
    
    # Relationships
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False, index=True)
    
    # Item details (denormalized for historical accuracy)
    item_name = db.Column(db.String(100), nullable=False)
    item_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    special_instructions = db.Column(db.Text)
    
    # Calculated fields
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
        CheckConstraint('item_price >= 0', name='check_item_price_positive'),
    )
    
    def __init__(self, **kwargs):
        super(OrderItem, self).__init__(**kwargs)
        self.calculate_total()
    
    def calculate_total(self):
        """Calculate the total price for this order item."""
        if self.item_price is not None and self.quantity is not None:
            self.total_price = float(self.item_price) * int(self.quantity)
    
    def to_dict(self):
        """Convert the order item to a dictionary."""
        return {
            'id': self.id,
            'menu_item_id': self.menu_item_id,
            'item_name': self.item_name,
            'item_price': float(self.item_price) if self.item_price else 0.0,
            'quantity': self.quantity,
            'total_price': float(self.total_price) if self.total_price else 0.0,
            'special_instructions': self.special_instructions,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
