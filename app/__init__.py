from flask import Flask, render_template, redirect, url_for, request, json
import requests
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

app = Flask(__name__)
SELF = "'self'"
INLINE = "'unsafe-inline'"
talisman = Talisman(
    app,
    content_security_policy={
        'img-src': '*',
        'script-src': [
            SELF,
            INLINE,
            '*.bootstrapcdn.com',
            'cdnjs.cloudflare.com',
            'ajax.googleapis.com',
            'code.jquery.com',
        ]
    },
    content_security_policy_nonce_in=['script-src', 'style-src'],
    strict_transport_security=False,
    force_https = False
)
app._static_folder = 'static/'
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'user.login'

from app.users.views import user_module

app.register_blueprint(user_module, url_prefix='/users')
