from functools import wraps

from flask import request

from models import User


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return _error_authenticate()

        if not _check_auth(auth.username, auth.password):
            return _error_authenticate()

        return f(*args, **kwargs)

    return decorated


def _error_authenticate():
    return {'message': 'Login Required'}, 401


def _check_auth(username, password):
    u = User.query.filter_by(username=username).first()
    if not u:
        return False
    return username == u.username and u.check_password(password)


def get_user():
    auth = request.authorization
    user = User.get(auth)
    return user
