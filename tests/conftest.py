"""Pytest fixtures for Flask application testing."""

import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db(app):
    """Create a fresh database for each test."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.rollback()
        _db.drop_all()


@pytest.fixture
def client(app, db):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture
def sample_user(db):
    """Create a sample user for testing."""
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    user = User(username='admin', email='admin@example.com', role='admin')
    user.set_password('admin123')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_client(client, sample_user):
    """Create an authenticated test client."""
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'password123',
    }, follow_redirects=True)
    return client
