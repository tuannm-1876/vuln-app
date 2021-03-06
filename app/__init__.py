from flask import Flask, render_template, redirect, url_for, request, json
import requests
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_seasurf import SeaSurf

app = Flask(__name__)
csrf = SeaSurf(app)
SELF = "'self'"
INLINE = "'unsafe-inline'"
talisman = Talisman(
    app,
    content_security_policy={
        'img-src': '*'
    },
    content_security_policy_nonce_in=['script-src', 'style-src'],
    strict_transport_security=False,
    force_https = False,
    session_cookie_secure = False
)
app._static_folder = 'static/'
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'user.login'

from app.users.views import user_module

app.register_blueprint(user_module, url_prefix='/users')
