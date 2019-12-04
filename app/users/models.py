from sqlalchemy.ext.declarative import declarative_base
from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.users import constants as USER

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), default='img/default.jpg')
    isAdmin = db.Column(db.Integer, default=USER.USER, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email.lower()
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return (self.id)

    def is_authenticated(self):
        return True

class Posts(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    isPrivate = db.Column(db.Integer, default=USER.PUBLIC)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    def __init__(self, user_id, content, isPrivate):
        self.user_id = user_id
        self.content = content
        self.isPrivate = isPrivate

    def get_id(self):
        return (self.id)

class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    def get_id(self):
        return (self.id)