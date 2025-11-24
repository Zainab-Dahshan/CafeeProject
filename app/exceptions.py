class ValidationError(ValueError):
    """Custom exception class for validation errors."""
    pass


class DatabaseError(Exception):
    """Custom exception class for database-related errors."""
    pass


class AuthenticationError(Exception):
    """Custom exception class for authentication errors."""
    pass


class AuthorizationError(Exception):
    """Custom exception class for authorization errors."""
    pass


class ResourceNotFoundError(Exception):
    """Custom exception class for resource not found errors."""
    pass


class BusinessRuleError(Exception):
    """Custom exception class for business rule violations."""
    pass


class ExternalServiceError(Exception):
    """Custom exception class for external service errors."""
    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code or 400
        self.payload = payload or {}

    def to_dict(self):
        """Convert the exception to a dictionary for JSON responses."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = 'error'
        rv['code'] = self.status_code
        return rv
