import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap3 import Bootstrap
from flask_migrate import Migrate
from flask_caching import Cache
from flask_moment import Moment
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'  # Prevents session fixation
bootstrap = Bootstrap()
migrate = Migrate()
cache = Cache()
moment = Moment()
mail = Mail()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    
    # Initialize security headers
    Talisman(
        app,
        force_https=app.config.get('SESSION_COOKIE_SECURE', False),
        strict_transport_security=True,
        session_cookie_secure=app.config.get('SESSION_COOKIE_SECURE', False),
        content_security_policy={
            'default-src': ["'self'"],
            'script-src': [
                "'self'",
                'cdn.jsdelivr.net',
                'code.jquery.com',
                'stackpath.bootstrapcdn.com',
                'cdnjs.cloudflare.com',
                "'unsafe-inline'"  # Required for some Bootstrap functionality
            ],
            'style-src': [
                "'self'",
                'cdn.jsdelivr.net',
                'stackpath.bootstrapcdn.com',
                'cdnjs.cloudflare.com',
                'fonts.googleapis.com',
                "'unsafe-inline'"
            ],
            'img-src': [
                "'self'",
                'data:',
                'blob:',
                '*.tile.openstreetmap.org',
                '*.tiles.mapbox.com',
                '*.gstatic.com',
                '*.googleapis.com',
                '*.bootstrapcdn.com',
                '*.fontawesome.com',
                '*.cloudflare.com',
                '*.jquery.com',
                '*.jsdelivr.net',
                '*.stripe.com',
                's3.amazonaws.com',
                '*.githubusercontent.com'
            ],
            'font-src': [
                "'self'",
                'data:',
                'fonts.gstatic.com',
                'fonts.googleapis.com',
                'cdnjs.cloudflare.com',
                'stackpath.bootstrapcdn.com',
                'use.fontawesome.com'
            ],
            'connect-src': [
                "'self'",
                '*.tiles.mapbox.com',
                'api.mapbox.com',
                'events.mapbox.com',
                '*.stripe.com',
                'sentry.io',
                '*.google-analytics.com',
                '*.doubleclick.net',
                '*.google.com',
                '*.gstatic.com',
                '*.cloudflare.com',
                '*.jsdelivr.net',
                '*.bootstrapcdn.com',
                '*.fontawesome.com',
                '*.jquery.com',
                '*.githubusercontent.com'
            ]
        },
        content_security_policy_nonce_in=['script-src'],
        feature_policy={
            'geolocation': "'self'",
            'camera': "'none'",
            'microphone': "'none'"
        },
        referrer_policy='strict-origin-when-cross-origin',
        permissions_policy={
            'geolocation': 'self',
            'camera': '()',
            'microphone': '()',
            'payment': '()',
            'sync-xhr': 'self'
        }
    )
    
    # Configure cache
    if config_name == 'production':
        cache.init_app(app, config={
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': 'instance/cache',
            'CACHE_DEFAULT_TIMEOUT': 300
        })
    else:
        cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    
    # Register blueprints with URL prefixes
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    
    # Apply rate limiting to auth routes
    auth_blueprint.before_request(
        limiter.limit(
            "100 per day;10 per hour",
            methods=["POST"],
            error_message='Too many requests. Please try again later.'
        )
    )
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # Initialize models and create database tables
    with app.app_context():
        # Import models
        from .models import init_app as init_models
        models = init_models()
        
        # Make models available in the app context
        app.models = models
        
        # Create database tables if they don't exist
        db.create_all()
        
        # Create default admin user if it doesn't exist
        from .models.user import User
        from werkzeug.security import generate_password_hash
        
        if not User.query.filter_by(email='admin@cafe.com').first():
            admin = User(
                email='admin@cafe.com',
                username='admin',
                password=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    
    return app