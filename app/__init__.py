from flask import Flask, render_template, redirect, url_for, request, json
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.users.views import user_module

app.register_blueprint(user_module, url_prefix='/users')
