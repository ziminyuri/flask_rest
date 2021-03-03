from functools import wraps
from flask import request, Response, jsonify
from models import User


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        if not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return jsonify('Unauthorized', 401, {
        'WWW-Authenticate': 'Basic realm="Login Required"'
    })



def check_auth(username, password):
    u = User.query.filter_by(username=username).first()
    if not u:
        return False
    return username == u.username and u.check_password(password)