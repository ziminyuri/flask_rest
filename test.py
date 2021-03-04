from app import client
import json
import base64

user_auth = base64.b64encode(b"14:14").decode("utf-8")

"""
def test_registration():
    # Регистрация пользователя

    user = {
        'email': '14@mail.ru',
        'username': '14',
        'password': '14'
    }
    response = client.post('/api/v1/registration', json=user)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == {
        'email': '14@mail.ru',
        'username': '14',
    }
"""


def test_get_users():
    # Получение списка пользователей после авторизации

    response = client.get('/api/v1/users',
    headers={"Authorization": "Basic " + user_auth})

    assert response.status_code == 200


def test_get_users_without_auth():
    # Получение списка пользователей без авторизации

    response = client.get('/api/v1/users')
    assert response.status_code == 401


def test_get_posts_without_auth():
    # Получение списка постов без авторизации

    response = client.get('/api/v1/posts')
    assert response.status_code == 200


def test_add_post_without_auth():
    # Добавление поста без авторизации

    post = {
        'title': 'Lorem ipsum dolor sit amet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer aliquet lectus ut quam ullamcorper laoreet. In vitae lectus suscipit ex suscipit accumsan. Mauris condimentum consectetur lectus ac sollicitudin. Nulla a mi tristique, bibendum arcu finibus, faucibus tellus. Maecenas elit arcu, cursus quis varius quis, efficitur eu lectus. Cras ac nulla ante. Maecenas posuere euismod augue, id mattis risus accumsan vitae.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer aliquet lectus ut quam ullamcorper laoreet. In vitae lectus suscipit ex suscipit accumsan. Mauris condimentum consectetur lectus ac sollicitudin. Nulla a mi tristique, bibendum arcu finibus, faucibus tellus. Maecenas elit arcu, cursus quis varius quis, efficitur eu lectus. Cras ac nulla ante. Maecenas posuere euismod augue, id mattis risus accumsan vitae.',
    }
    response = client.post('/api/v1/posts', json=post)
    assert response.status_code == 401


def test_add_post_with_auth_with_error_with_content_length():
    # Добавление поста с авторизацией пользователя. В данных есть ошибка, длина content больше 500

    post = {
        'title': 'Lorem ipsum dolor sit amet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer aliquet lectus ut quam ullamcorper laoreet. In vitae lectus suscipit ex suscipit accumsan. Mauris condimentum consectetur lectus ac sollicitudin. Nulla a mi tristique, bibendum arcu finibus, faucibus tellus. Maecenas elit arcu, cursus quis varius quis, efficitur eu lectus. Cras ac nulla ante. Maecenas posuere euismod augue, id mattis risus accumsan vitae.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer aliquet lectus ut quam ullamcorper laoreet. In vitae lectus suscipit ex suscipit accumsan. Mauris condimentum consectetur lectus ac sollicitudin. Nulla a mi tristique, bibendum arcu finibus, faucibus tellus. Maecenas elit arcu, cursus quis varius quis, efficitur eu lectus. Cras ac nulla ante. Maecenas posuere euismod augue, id mattis risus accumsan vitae.',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 400

    error = {
        "message": {
            "json": {
                "content": ["Longer than maximum length 500."]
            }
        }
    }

    data = json.loads(response.data)
    assert data == error


def test_add_post_with_auth():
    # Добавление и удаление поста с авторизацией пользователя .

    post = {
        'title': 'Lorem ipsum dolor sit amet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['content'] == post['content']
    assert data['title'] == post['title']

    id = data['id']

    response = client.delete('/api/v1/posts/' + str(id))
    assert response.status_code == 401

    response = client.delete('/api/v1/posts/'+str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204


def test_update_post_with_auth():
    # Редактирование (перед этим добавление) с авторизацией пользователя и без, удаление поста.

    post = {
        'title': 'Lorem ipsum dolor sit amet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    assert data_after_add['title'] == post['title']

    id = data_after_add['id']

    post_update_title = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
    }
    response = client.put('/api/v1/posts/' + str(id), json=post_update_title)
    assert response.status_code == 401

    response = client.put('/api/v1/posts/'+str(id), json=post_update_title,
                             headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_update = json.loads(response.data)
    assert data_after_update['title'] == post_update_title['title']
    assert data_after_add['title'] != data_after_update['title']

    response = client.delete('/api/v1/posts/'+str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204


def test_update_not_user_post():
    # Пост добавляется одним пользователем, а попытка изменить другим

    post = {
        'title': 'Lorem ipsum dolor sit amet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    id = data_after_add['id']

    post_update_title = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
    }
    another_user = base64.b64encode(b"4:44").decode("utf-8")
    response = client.put('/api/v1/posts/' + str(id), json=post_update_title,
                          headers={"Authorization": "Basic " + another_user})

    assert response.status_code == 400
    error = {
        'message': 'No post with this id'
    }

    data = json.loads(response.data)
    assert data == error

    response = client.put('/api/v1/posts/' + str(id), json=post_update_title,
                          headers={"Authorization": "Basic " + user_auth})

    assert response.status_code == 200

    response = client.delete('/api/v1/posts/' + str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204


def test_update_datetime_of_post():
    # Добавление и обновление даты публикации поста

    post = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    id = data_after_add['id']

    post_update = {
        'title': '143223',
        'publication_datetime': '2021-02-03T13:48:05.686613'
    }

    response = client.put('/api/v1/posts/' + str(id), json=post_update,
                          headers={"Authorization": "Basic " + user_auth})

    assert response.status_code == 200
    data_after_update = json.loads(response.data)
    assert data_after_update['publication_datetime'] == post_update['publication_datetime']
    assert data_after_update['publication_datetime'] != data_after_add['publication_datetime']

    response = client.delete('/api/v1/posts/' + str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204


def test_add_post_without_content():
    # Добавление поста, в содержимом только заголовок без поля content

    post = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
    }

    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 400

    error = {
        "message": {
            "json": {
                "content": [
                    "Missing data for required field."
                ]
            }
        }
    }

    data = json.loads(response.data)
    assert data == error


def test_add_comment():
    # Добавление комментария пользователем к созданном посту

    post = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    id = data_after_add['id']

    comment = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }

    response = client.post('/api/v1/posts/'+str(id)+'/comments', json=comment,
                           headers={"Authorization": "Basic " + user_auth})

    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    comment_id = data_after_add['id']

    response = client.delete('/api/v1/posts/' + str(id)+'/comments/'+str(comment_id),
                             headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204

    response = client.delete('/api/v1/posts/' + str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204


def test_delete_comment():
    # Добавление комментария пользователем к созданном посту, удаление не авторизованным пользователем, авторизованным,
    # но не автором комметария, и автором комментария

    post = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }
    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    id = data_after_add['id']

    comment = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }

    response = client.post('/api/v1/posts/'+str(id)+'/comments', json=comment,
                           headers={"Authorization": "Basic " + user_auth})

    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    comment_id = data_after_add['id']

    response = client.delete('/api/v1/posts/' + str(id)+'/comments/'+str(comment_id))
    assert response.status_code == 401

    another_user = base64.b64encode(b"4:44").decode("utf-8")
    response = client.delete('/api/v1/posts/' + str(id) + '/comments/' + str(comment_id),
                             headers={"Authorization": "Basic " + another_user})

    assert response.status_code == 400
    error = {
        'message': 'No comment with this id'
    }

    data = json.loads(response.data)
    assert data == error

    response = client.delete('/api/v1/posts/' + str(id)+'/comments/'+str(comment_id),
                             headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204

    response = client.delete('/api/v1/posts/' + str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204


def test_update_comment():
    # Добавление комментария пользователем к созданном посту, обновление комментария не авторизованным пользователем, авторизованным,
    # но не автором комметария, и автором комментария
    # удаление комментраия автором

    post = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }

    response = client.post('/api/v1/posts', json=post, headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    id = data_after_add['id']

    comment = {
        'title': 'Lor423432em fdsfds342ipsum dolor sit aet.',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ',
    }

    response = client.post('/api/v1/posts/' + str(id) + '/comments', json=comment,
                           headers={"Authorization": "Basic " + user_auth})

    assert response.status_code == 200

    data_after_add = json.loads(response.data)
    comment_id = data_after_add['id']

    update_comment = {
        'title': 'Lor423434322em fdsfds342ipsum dolor sit aet.',
    }

    response = client.put('/api/v1/posts/' + str(id) + '/comments/' + str(comment_id),json=update_comment)
    assert response.status_code == 401

    another_user = base64.b64encode(b"4:44").decode("utf-8")
    response = client.put('/api/v1/posts/' + str(id) + '/comments/' + str(comment_id), json=update_comment,
                             headers={"Authorization": "Basic " + another_user})

    assert response.status_code == 400
    error = {
        'message': 'No comment with this id'
    }

    data = json.loads(response.data)
    assert data == error

    response = client.put('/api/v1/posts/' + str(id) + '/comments/' + str(comment_id), json=update_comment,
                             headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 200
    data_after_update = json.loads(response.data)
    assert data_after_update['title'] == update_comment['title']
    assert data_after_update['title'] != data_after_add['title']

    response = client.delete('/api/v1/posts/' + str(id) + '/comments/' + str(comment_id),
                             headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204

    response = client.delete('/api/v1/posts/' + str(id), headers={"Authorization": "Basic " + user_auth})
    assert response.status_code == 204