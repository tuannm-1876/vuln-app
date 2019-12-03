import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost:3306/vuvln_app'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '\x9c$f\xaf\xa4\xb1g\xf2\x0e-\xdb^ym\xf6\xd7\x9dO\xf0\t\x13\xcf\xce\x13'

UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'files')