from flask_wtf import Form
from wtforms import TextField, SubmitField, validators, PasswordField, HiddenField
from app.users.models import Users
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(Form)


class UserForm(ModelForm):
    class Meta:
        model = Users
        only = ['name', 'email']


class SignupForm(Form):
    email = TextField('Email address',  [
        validators.Required('Please enter your email address.'),
        validators.Email('Please enter your email address.')
    ])
    username = TextField('Username',  [
        validators.Required('Please enter your username.'),
        validators.Length(
            max=30, message='Username is at most 30 characters.'),
    ])
    name = TextField('Name',  [
        validators.Required('Please enter your name.'),
        validators.Length(
            max=30, message='Name is at most 30 characters.'),
    ])
    password = PasswordField('Password', [
        validators.Required('Please enter a password.'),
        validators.Length(
            min=6, message='Passwords is at least 6 characters.'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Sign up')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = Users.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('That username is already taken.')
            return False
        user_email = Users.query.filter_by(email=self.email.data).first()
        if user_email:
            self.username.errors.append('That email is already taken.')
            return False

        return True


class LoginForm(Form):
    email = TextField('email',  [
        validators.Required('Please enter your email.'),
        validators.Length(max=45, message='Email is at most 45 characters.'),
    ])
    password = PasswordField('password', [
        validators.Required('Please enter a password.'),
        validators.Length(
            min=6, message='Passwords is at least 6 characters.'),
    ])
    submit = SubmitField('login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        user = Users.query.filter_by(email=self.email.data).first()
        if user:
            if not user.check_password(self.password.data):
                self.password.errors.append('Wrong password')
                return False
            else:
                return True
        else:
            self.password.errors.append('Invalid e-mail or password')
            return False

