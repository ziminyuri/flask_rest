from flask import Flask, jsonify, request
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec
from flask_apispec.extension import FlaskApiSpec
from schemas import UserSchema
from flask_apispec import use_kwargs, marshal_with

app = Flask(__name__)


client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

docs = FlaskApiSpec()
docs.init_app(app)

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='blog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    ),
    'APISPEC_SWAGGER_URL': '/swagger'
})

from models import User
Base.metadata.create_all(bind=engine)
from services.auth import login_required


@app.route('/api/v1/registration', methods=['POST'])
@marshal_with(UserSchema)
def registration():
    body = request.get_json()
    email = body['email']
    username = body['username']
    password = body['password']
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    session.add(new_user)
    session.commit()
    return new_user


@app.route('/api/v1/users', methods=['GET'])
@login_required
@marshal_with(UserSchema(many=True))
def get_users():
    users = User.query.all()
    return users


@app.route('/api/v1/users', methods=['POST'])
def add_users():
    new_user = User(**request.json)
    session.add(new_user)
    session.commit()

    serialized = {
        'email': new_user.email,
        'username': new_user.username,
        'password': new_user.password
    }
    return jsonify(serialized)


@app.route('/api/v1/users/<int:username>', methods=['PUT'])
def update_user(username):
    user = User.query.filter(User.username == username).first()
    params = request.json
    if not user:
        return {'message': 'No users with this username'}, 400

    for key, value in params.items():
        setattr(user, key, value)
    session.commit()
    serialized = {
        'email': user.email,
        'username': user.username,
        'password': user.password
    }
    return serialized


@app.route('/api/v1/users/<int:username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter(User.username == username).first()

    if not user:
        return {'message': 'No users with this username'}, 400

    session.delete(user)
    session.commit()

    return '', 204

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True)
