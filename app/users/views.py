from flask import render_template, redirect, url_for, request, Blueprint, flash, g, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app.users.forms import LoginForm, SignupForm
from app.users.models import Users
from flask_sqlalchemy import SQLAlchemy
from app import app, db, lm
user_module = Blueprint('users', __name__)


@user_module.route("/")
def welcome():
    return redirect(url_for('index'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@user_module.route('/signin', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Logged in successfully.', category='success')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('signin.html', form=form)

@user_module.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category='success')
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('session')
    return redirect(url_for('index'))

@user_module.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        new_user = Users(form.username.data, form.name.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup in successfully.', category='success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)


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


def check_user(email, password):
    user = Users.query.filter_by(email=email).first()
    if not user:
        return (False, 'User does not exist')
    if user.check_password(password):
        return (True, 'Success')
    else:
        return (False, 'Incorrect password')
