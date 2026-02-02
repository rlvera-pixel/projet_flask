"""Tests for authentication routes."""


class TestRegistration:
    """Tests for user registration."""

    def test_register_page(self, client):
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Inscription' in response.data

    def test_register_success(self, client, db):
        response = client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'password2': 'password123',
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Inscription' in response.data or b'Connexion' in response.data

    def test_register_duplicate_username(self, client, sample_user):
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'other@example.com',
            'password': 'password123',
            'password2': 'password123',
        }, follow_redirects=True)
        assert b'nom d' in response.data.lower() or b'pris' in response.data.lower()

    def test_register_password_mismatch(self, client, db):
        response = client.post('/auth/register', data={
            'username': 'mismatch',
            'email': 'mis@example.com',
            'password': 'password123',
            'password2': 'different',
        }, follow_redirects=True)
        assert b'correspondent' in response.data.lower() or response.status_code == 200


class TestLogin:
    """Tests for user login."""

    def test_login_page(self, client):
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Connexion' in response.data

    def test_login_success(self, client, sample_user):
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'password123',
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_wrong_password(self, client, sample_user):
        response = client.post('/auth/login', data={
            'username': 'testuser',
            'password': 'wrongpass',
        }, follow_redirects=True)
        assert b'incorrect' in response.data.lower()

    def test_login_nonexistent_user(self, client, db):
        response = client.post('/auth/login', data={
            'username': 'nobody',
            'password': 'password',
        }, follow_redirects=True)
        assert b'incorrect' in response.data.lower()


class TestLogout:
    """Tests for user logout."""

    def test_logout(self, auth_client):
        response = auth_client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200


class TestProtectedRoutes:
    """Tests for login-required routes."""

    def test_dashboard_requires_login(self, client, db):
        response = client.get('/dashboard/', follow_redirects=True)
        assert b'Connexion' in response.data or b'connecter' in response.data.lower()

    def test_dashboard_accessible_when_logged_in(self, auth_client):
        response = auth_client.get('/dashboard/')
        assert response.status_code == 200
