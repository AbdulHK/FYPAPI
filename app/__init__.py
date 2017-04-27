from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import secure_filename
app = Flask(__name__,static_url_path='')
app.config.from_object('config')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from .call import authien
from .routes import users
from .routes import hours
from .routes import pref
from .routes import restaurant
from .routes import review
from .routes import menu