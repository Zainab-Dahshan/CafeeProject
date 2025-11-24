from flask import Blueprint
from flask_login import current_user, login_required

# Create the authentication blueprint
auth = Blueprint('auth', __name__)

# Import routes at the bottom to avoid circular imports
from . import routes
