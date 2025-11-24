from flask import render_template, request, jsonify
from .. import db
from . import main
from ..exceptions import ValidationError


def bad_request(message):
    """Return a 400 Bad Request response."""
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    """Return a 401 Unauthorized response."""
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    """Return a 403 Forbidden response."""
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@main.app_errorhandler(400)
def bad_request_error(error):
    """Handle 400 Bad Request errors."""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'bad request',
            'message': 'The request cannot be fulfilled due to bad syntax.'
        })
        response.status_code = 400
        return response
    return render_template('errors/400.html'), 400


@main.app_errorhandler(401)
def unauthorized_error(error):
    """Handle 401 Unauthorized errors."""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'unauthorized',
            'message': 'Authentication is required to access this resource.'
        })
        response.status_code = 401
        return response
    return render_template('errors/401.html'), 401


@main.app_errorhandler(403)
@main.app_errorhandler(404)
def page_not_found(error):
    """Handle 404 Not Found errors."""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'not found',
            'message': 'The requested resource was not found.'
        })
        response.status_code = 404
        return response
    return render_template('errors/404.html'), 404


@main.app_errorhandler(403)
def forbidden_error(error):
    """Handle 403 Forbidden errors."""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'forbidden',
            'message': 'You do not have permission to access this resource.'
        })
        response.status_code = 403
        return response
    return render_template('errors/403.html'), 403


@main.app_errorhandler(413)
def request_entity_too_large_error(error):
    """Handle 413 Request Entity Too Large errors."""
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'request entity too large',
            'message': 'The data value transmitted exceeds the capacity limit.'
        })
        response.status_code = 413
        return response
    return render_template('errors/413.html'), 413


@main.app_errorhandler(500)
def internal_server_error(error):
    """Handle 500 Internal Server errors."""
    db.session.rollback()
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({
            'error': 'internal server error',
            'message': 'An unexpected error has occurred.'
        })
        response.status_code = 500
        return response
    return render_template('errors/500.html'), 500


@main.app_errorhandler(ValidationError)
def validation_error(e):
    """Handle validation errors."""
    return bad_request(e.args[0])
