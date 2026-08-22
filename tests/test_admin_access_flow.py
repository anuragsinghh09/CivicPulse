import sys
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'backend'))

from app import create_app
from app.extensions import db
from app.models import User


@pytest.fixture()
def app():
    application = create_app({
        'TESTING': True,
        'SECRET_KEY': 'test-secret',
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with application.app_context():
        db.drop_all()
        db.create_all()
        password_hash = generate_password_hash('valid-test-password')
        db.session.add_all([
            User(
                user_id=1,
                full_name='Test Citizen',
                email='citizen@test.local',
                phone='0000000001',
                password_hash=password_hash,
                role='Citizen',
            ),
            User(
                user_id=2,
                full_name='Test Admin',
                email='admin@test.local',
                phone='0000000002',
                password_hash=password_hash,
                role='Admin',
            ),
        ])
        db.session.commit()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def login(client, path, email, password='valid-test-password'):
    return client.post(path, data={
        'email' if path == '/public/login' else 'admin-email': email,
        'password' if path == '/public/login' else 'admin-password': password,
    })


def test_citizen_login_through_public_login(client):
    response = login(client, '/public/login', 'citizen@test.local')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/citizen/dashboard')


def test_admin_is_redirected_to_dedicated_login_from_public_login(client):
    response = login(client, '/public/login', 'admin@test.local')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/admin/login')
    assert b'dedicated admin login' in client.get(response.headers['Location']).data
    assert client.get('/admin/dashboard').status_code == 302


def test_admin_login_through_dedicated_login(client):
    response = login(client, '/admin/login', 'admin@test.local')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/admin/dashboard')
    assert client.get('/admin/dashboard').status_code == 200


def test_citizen_cannot_login_through_admin_login(client):
    response = login(client, '/admin/login', 'citizen@test.local')

    assert response.status_code == 200
    assert b'Invalid admin credentials.' in response.data
    assert client.get('/admin/dashboard').status_code == 302


def test_authenticated_citizen_cannot_access_admin_dashboard(client):
    login(client, '/public/login', 'citizen@test.local')

    response = client.get('/admin/dashboard')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/public/home')


def test_authenticated_admin_can_access_admin_dashboard(client):
    login(client, '/admin/login', 'admin@test.local')

    response = client.get('/admin/dashboard')

    assert response.status_code == 200


def test_citizen_logout_ends_session(client):
    login(client, '/public/login', 'citizen@test.local')

    response = client.get('/logout')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/public/home')
    assert client.get('/citizen/dashboard').status_code == 302


def test_admin_logout_ends_session(client):
    login(client, '/admin/login', 'admin@test.local')

    response = client.get('/logout')

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/public/home')
    assert client.get('/admin/dashboard').status_code == 302
