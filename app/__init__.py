from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
app = Flask(__name__,static_url_path='')
app.config.from_object('config')

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

import call.authien
import routes.users
import routes.hours
import routes.pref
import routes.restaurant
import routes.review
import routes.menu