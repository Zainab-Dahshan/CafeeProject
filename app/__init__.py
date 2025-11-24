from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate
from flask_caching import Cache
from flask_moment import Moment
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap5()
migrate = Migrate()
cache = Cache()
moment = Moment()

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
    cache.init_app(app)
    moment.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    # Error handlers
    from .utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db}
    
    return app
