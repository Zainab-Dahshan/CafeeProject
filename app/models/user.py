from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .base import db, BaseModel
from datetime import datetime
import uuid

class User(UserMixin, BaseModel):
    """User model for authentication and profile information."""
    __tablename__ = 'users'
    
    # Basic information
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Profile information
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    profile_image = db.Column(db.String(255))
    
    # Timestamps
    last_login_at = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='customer', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email:
            self.email = self.email.lower()
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('Password is not a readable attribute.')
    
    @password.setter
    def password(self, password):
        """Set password to a hashed password."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        """Check if hashed password matches actual password."""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    
    def update_last_seen(self):
        """Update the last seen timestamp."""
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    
    def generate_auth_token(self, expiration=3600):
        """Generate an authentication token for the user."""
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        from flask import current_app
        
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_auth_token(token):
        """Verify the authentication token and return the user."""
        from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        from itsdangerous import SignatureExpired, BadSignature
        from flask import current_app
        
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except (SignatureExpired, BadSignature):
            return None
        
        return User.query.get(data['id'])
    
    def __repr__(self):
        return f'<User {self.username}>'
