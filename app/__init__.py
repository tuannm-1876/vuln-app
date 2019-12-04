from flask import Flask, render_template, redirect, url_for, request, json
import requests
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app._static_folder = 'static/'
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'user.login'

from app.users.views import user_module

app.register_blueprint(user_module, url_prefix='/users')
