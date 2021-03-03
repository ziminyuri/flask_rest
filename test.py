from app import client


def test_get_users():
    response = client.get('/api/v1/users')

    assert response.status_code == 200


def test_add_user():
    user = {
        'email': '8@mail.ru',
        'username': '8',
        'password': '12345423'
    }
    response = client.post('/api/v1/users', json=user)

    assert response.status_code == 200
    assert response == {
        'email': '8@mail.ru',
        'username': '8',
    }
