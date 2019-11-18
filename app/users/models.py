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
    avatar = db.Column(db.String(255), default='/img/avatar/default.jpg')
    isAdmin = db.Column(db.Integer, default=USER.USER, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Integer, default=0)
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
