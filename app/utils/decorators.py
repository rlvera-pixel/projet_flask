"""Custom decorators for route protection."""

from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    """Decorator that restricts access to admin users only.

    Usage:
        @app.route('/admin')
        @login_required
        @admin_required
        def admin_panel():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
