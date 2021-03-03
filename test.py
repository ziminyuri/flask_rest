from app import client


def test_get_users():
    response = client.get('/users')

    assert response.status_code == 200


def test_add_user():
    user = {
        'email': '1@mail.ru',
        'username': '1',
        'password': '12345'
    }
    response = client.post('/users', json=user)

    assert response.status_code == 200
