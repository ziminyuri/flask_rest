from flask import jsonify, request
from flask_apispec import marshal_with, use_kwargs

from app import app, logger, session
from models import Comment, Post, User
from schemas import (CommentSchema, CommentSchemaForUpdate, PostSchema,
                     PostSchemaForUpdate, UserSchema)
from services.auth import get_user, login_required


@app.route('/api/v1/registration', methods=['POST'])
@marshal_with(UserSchema)
def registration():
    try:
        body: dict = request.json
        new_user: object = User(**body)
        session.add(new_user)
        session.commit()
    except Exception as e:
        logger.warning(
            f'users: - add user action failed with error: {e}'
        )
        return {'message': str(e)}, 400
    return new_user


@app.route('/api/v1/users', methods=['GET'])
@login_required
@marshal_with(UserSchema(many=True))
def get_users():
    try:
        users: list = User.query.all()
    except Exception as e:
        return {'message': str(e)}, 400
    return users


@app.route('/api/v1/posts', methods=['GET'])
@marshal_with(PostSchema(many=True))
def get_posts():
    try:
        posts: list = Post.get_posts()
    except Exception as e:
        logger.warning(
            f'post: - get posts action failed with error: {e}'
        )
        return {'message': str(e)}, 400
    return posts


@app.route('/api/v1/posts', methods=['POST'])
@login_required
@use_kwargs(PostSchema)
@marshal_with(PostSchema)
def add_post(**kwargs):
    try:
        user = get_user()
        new_post = Post(author_id=user.username, **kwargs)
        new_post.save()
    except Exception as e:
        logger.warning(
            f'user: {user.username} post: - add post action failed with error: {e}'
        )
        return {'message': str(e)}, 400
    return new_post


@app.route('/api/v1/posts/<int:post_id>', methods=['PUT'])
@login_required
@use_kwargs(PostSchemaForUpdate)
@marshal_with(PostSchema)
def update_post(post_id, **kwargs):
    try:
        user: object = get_user()
        post: object = Post.get(post_id, user)
        post.update(**kwargs)
    except Exception as e:
        logger.warning(
            f'user: {user.username} post: - update post action failed with error: {e}'
        )
        return {'message': str(e)}, 400

    return post


@app.route('/api/v1/posts/<int:post_id>', methods=['DELETE'])
@login_required
@marshal_with(PostSchema)
def delete_post(post_id):
    try:
        user: object = get_user()
        post: object = Post.get(post_id, user)
        post.delete()

    except Exception as e:
        logger.warning(
            f'user: {user.username} post: - delete post action failed with error: {e}'
        )
        return {'message': str(e)}, 400

    return '', 204


@app.route('/api/v1/posts/<int:post_id>/comments', methods=['GET'])
@marshal_with(CommentSchema(many=True))
def get_comments(post_id):
    try:
        comments = Comment.get_comments(post_id)
    except Exception as e:
        logger.warning(
            f'comments: - get comments action failed with error: {e}'
        )
        return {'message': str(e)}, 400
    return comments


@app.route('/api/v1/posts/<int:post_id>/comments', methods=['POST'])
@login_required
@use_kwargs(CommentSchema)
@marshal_with(CommentSchema)
def add_comment(post_id, **kwargs):
    try:
        user = get_user()
        new_comment = Comment(author_id=user.username, **kwargs, post_id=post_id)
        new_comment.save()
    except Exception as e:
        logger.warning(
            f'user: {user.username} post: {post_id} comment: - add comment action failed with error: {e}'
        )
        return {'message': str(e)}, 400
    return new_comment


@app.route('/api/v1/posts/<int:post_id>/comments/<int:comment_id>', methods=['PUT'])
@login_required
@use_kwargs(CommentSchemaForUpdate)
@marshal_with(CommentSchema)
def update_comment(post_id, comment_id, **kwargs):
    try:
        user = get_user()
        comment = Comment.get(post_id,  user, comment_id)
        comment.update(**kwargs)
    except Exception as e:
        logger.warning(
            f'user: {user.username} post: {post_id} comment: - update comment action failed with error: {e}'
        )
        return {'message': str(e)}, 400

    return comment


@app.route('/api/v1/posts/<int:post_id>/comments/<int:comment_id>', methods=['DELETE'])
@login_required
@marshal_with(CommentSchema)
def delete_comment(post_id, comment_id):
    try:
        user = get_user()
        post = Comment.get(post_id, user, comment_id)
        post.delete()

    except Exception as e:
        logger.warning(
            f'user: {user.username} post: {post_id} comment: - delete comment action failed with error: {e}'
        )
        return {'message': str(e)}, 400

    return {''}, 204


@app.errorhandler(422)
def error_handler(error):
    headers = error.data.get('headers', None)
    messages = error.data.get('messages', ['Invalid request'])
    if headers:
        return jsonify({'message': messages}), 400, headers
    else:
        return jsonify({'message': messages}), 400

