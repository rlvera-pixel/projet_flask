"""WSGI entry point for production deployment (Gunicorn).

Usage:
    gunicorn wsgi:app
"""

import os
from app import create_app

config_name = os.environ.get('FLASK_CONFIG', 'production')
app = create_app(config_name)
