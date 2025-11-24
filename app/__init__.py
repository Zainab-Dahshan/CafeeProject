from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap3 import Bootstrap
from flask_migrate import Migrate
from flask_caching import Cache
from flask_moment import Moment
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()
migrate = Migrate()  # Initialize Flask-Migrate
cache = Cache()
moment = Moment()

# Import models after extensions to avoid circular imports
# This import needs to be after db initialization but before create_app
# The actual model classes will be imported when needed

def create_app(config_name='default'):
    """Application factory function."""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    migrate.init_app(app, db)  # Initialize with both app and db
    cache.init_app(app)
    moment.init_app(app)
    
    # Import and register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Import models after app is created to avoid circular imports
    with app.app_context():
        # Initialize models and get model classes
        from .models import init_app as init_models
        models = init_models(app)
        
        # Make models available in the app context
        app.models = models
        
        # Create database tables if they don't exist
        db.create_all()
    
    return app