"""Application factory for the Flask app."""

import logging
from flask import Flask
from app.config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name='default'):
    """Create and configure the Flask application.

    Args:
        config_name: Configuration name ('development', 'production', 'testing', 'default').

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.errors import errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(errors_bp)

    # Register before/after request hooks
    register_hooks(app)

    # Register custom Jinja2 filters
    register_filters(app)

    # Ensure upload folder exists
    import os
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Configure logging
    configure_logging(app)

    return app


def register_hooks(app):
    """Register before/after request hooks for middleware-like behavior."""
    @app.before_request
    def log_request():
        import time
        from flask import g, request
        g.start_time = time.time()
        app.logger.debug('Request: %s %s', request.method, request.path)

    @app.after_request
    def log_response(response):
        import time
        from flask import g, request
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            app.logger.debug(
                'Response: %s %s %s (%.3fs)',
                request.method, request.path, response.status_code, elapsed
            )
        return response


def register_filters(app):
    """Register custom Jinja2 template filters."""
    @app.template_filter('datetime')
    def format_datetime(value, fmt='%d/%m/%Y %H:%M'):
        """Format a datetime object."""
        if value is None:
            return ''
        return value.strftime(fmt)

    @app.template_filter('filesizeformat')
    def filesizeformat(value):
        """Format file size in human-readable format."""
        for unit in ['o', 'Ko', 'Mo', 'Go']:
            if value < 1024:
                return f'{value:.1f} {unit}'
            value /= 1024
        return f'{value:.1f} To'

    @app.template_filter('truncate_words')
    def truncate_words(s, num=30):
        """Truncate a string to a given number of words."""
        words = s.split()
        if len(words) <= num:
            return s
        return ' '.join(words[:num]) + '...'


def configure_logging(app):
    """Configure application logging."""
    if not app.debug and not app.testing:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
