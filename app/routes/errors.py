"""Error handlers blueprint."""

from flask import Blueprint, render_template, jsonify, request

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Accès interdit.'}), 403
    return render_template('errors/403.html'), 403


@errors_bp.app_errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Ressource non trouvée.'}), 404
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors."""
    from app.extensions import db
    db.session.rollback()
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Erreur interne du serveur.'}), 500
    return render_template('errors/500.html'), 500
