import os
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = "Hello there my name is Abdul"
link= 'mysql://Abdul:Abdul1993@ec2-52-24-39-230.us-west-2.compute.amazonaws.com/test'
SQLALCHEMY_DATABASE_URI = link
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = '/Users/abdulhakim/Documents/Code/API.v2/static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

