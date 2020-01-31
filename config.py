import os
basedir = os.path.abspath(os.path.dirname(__file__))
username = os.environ['MYSQL_USER']
password = os.environ['MYSQL_PASSWORD']
database = os.environ['MYSQL_DATABASE']
SQLALCHEMY_DATABASE_URI = 'mysql://'+username + \
    ':'+password+'@db-vulnapp:3306/'+database
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ['SECRET_KEY']

UPLOAD_FOLDER = os.path.join(basedir, 'app', 'static', 'files')
