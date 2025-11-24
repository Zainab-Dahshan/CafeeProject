import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'csrf-secret-key-change-in-production'
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB max file size
    
    # Email settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@cafewebsite.com')
    
    # Application settings
    CAFE_MAIL_SUBJECT_PREFIX = '[Café] '
    CAFE_ADMIN = os.environ.get('ADMIN_EMAIL', 'admin@cafewebsite.com')
    APP_NAME = 'Café Website'
    APP_VERSION = '1.0.0'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app-dev.db')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Rate limiting
    RATELIMIT_DEFAULT = '200 per day;50 per hour'
    
    # Logging
    LOG_LEVEL = 'WARNING'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Caching
    CACHE_TYPE = 'RedisCache'  # Requires Redis server
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # File uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    
    # API settings
    API_PREFIX = '/api/v1'

class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # Log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get the appropriate configuration class based on the FLASK_ENV environment variable."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])