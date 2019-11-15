from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.users.models import Users
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from app import db

def add_user(email, name, username, password, repassword):
    user = Users.query.filter_by(username=username).first()
    if user:
        return (False, 'User already exists')
    if len(password) < 6:
        return (False, 'Password too short')
    if password != repassword:
        return (False, 'Password do not match')
    new_user = Users(email=email,
                    name=name,
                    username=username,
                    password=password)
    db.session.add(new_user)
    db.session.commit()

def user_exists(username):
    user = Users.query.filter_by(username=username).first()
    if not user:
        return (False, 'User does not exist')
    else:
        return (True, 'User exist')

def check_user(email, password):
    user = Users.query.filter_by(email=email).first()
    if not user:
        return (False, 'User does not exist')
    if user.check_password(password):
        return (True, user.username)
    else:
        return (False, 'Incorrect password')

def get_session():
    return db.session()
if __name__ == '__main__':
    print (check_user('minhtuanact@gmail.com', 'admin@123'))
