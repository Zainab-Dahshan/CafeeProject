from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap3 import Bootstrap
from flask_migrate import Migrate
from flask_caching import Cache
from flask_moment import Moment
from flask_mail import Mail
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bootstrap = Bootstrap()
migrate = Migrate()
cache = Cache()
moment = Moment()
mail = Mail()

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
    
    # Configure cache
    if config_name == 'production':
        cache.init_app(app, config={
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': 'instance/cache',
            'CACHE_DEFAULT_TIMEOUT': 300
        })
    else:
        cache.init_app(app, config={'CACHE_TYPE': 'simple'})
    
    # Register blueprints
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    
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