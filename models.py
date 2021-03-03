from app import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from werkzeug.security import generate_password_hash,  check_password_hash


class User(Base):
    __tablename__ = 'users'

    email = Column(String(50), nullable=False)
    username = Column(String(50), primary_key=True)
    password = Column(String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(500), nullable=False)
    publication_datetime = Column(DateTime)
    author_id = Column(String(50), ForeignKey('users.username'))


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String(255), nullable=False)
    publication_datetime = Column(DateTime)
    author_id = Column(String(50), ForeignKey('users.username'))
    post_id = Column(Integer, ForeignKey('posts.id'))
