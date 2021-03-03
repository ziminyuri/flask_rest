import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app import Base, session


class User(Base):
    __tablename__ = 'users'

    email = Column(String(50), nullable=False)
    username = Column(String(50), primary_key=True)
    password = Column(String(255), nullable=False)
    posts = relationship('Post', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __init__(self, **kwargs):
        try:
            self.email = kwargs.get('email')
            self.username = kwargs.get('username')
            self.password = generate_password_hash(kwargs.get('password'))
        except Exception:
            session.rollback()
            raise

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def get(cls, user):
        try:
            user = cls.query.filter_by(username=user.username).first()

            if not user:
                raise

        except Exception:
            session.rollback()
            raise

        return user


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(500), nullable=False)
    author_id = Column(String(50), ForeignKey('users.username'))
    publication_datetime = Column(DateTime)
    comments = relationship('Comment', backref='post', lazy=True)

    def __init__(self, author_id, **kwargs):
        try:
            self.title = kwargs.get('title')
            self.content = kwargs.get('content')
            self.author_id = author_id
            self.publication_datetime = kwargs.get('publication_datetime', datetime.datetime.now())

        except Exception as e:
            session.rollback()
            raise

    @classmethod
    def get_posts(cls):
        try:
            posts = cls.query.all()
            session.commit()
        except Exception:
            session.rollback()
            raise
        return posts

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get(cls, post_id, user):
        try:
            post = cls.query.filter(cls.id == post_id, cls.author_id == user.username).first()

            if not post:
                raise Exception ('No post with this id')

        except Exception:
            session.rollback()
            raise

        return post

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()

        except Exception:
            session.rollback()
            raise


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    publication_datetime = Column(DateTime)
    author_id = Column(String(50), ForeignKey('users.username'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __init__(self, author_id, post_id, **kwargs):
        try:
            self.title = kwargs.get('title')
            self.content = kwargs.get('content')
            self.author_id = author_id
            self.post_id = post_id
            self.publication_datetime = kwargs.get('publication_datetime', datetime.datetime.now())

        except Exception as e:
            session.rollback()
            raise

    @classmethod
    def get_comments(cls, post_id):
        try:
            comments = cls.query.filter(cls.post_id==post_id)
            session.commit()
        except Exception:
            session.rollback()
            raise
        return comments

    def save(self):
        try:
            session.add(self)
            session.commit()
        except Exception:
            session.rollback()
            raise

    @classmethod
    def get(cls, post_id, user, comment_id):
        try:
            comment = cls.query.filter(cls.post_id == post_id, cls.author_id == user.username, cls.id == comment_id).first()

            if not comment:
                raise Exception('No comment with this id')

        except Exception:
            session.rollback()
            raise

        return comment

    def update(self, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self):
        try:
            session.delete(self)
            session.commit()

        except Exception:
            session.rollback()
            raise