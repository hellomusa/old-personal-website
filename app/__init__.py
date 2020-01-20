from flask import Flask
from flask_bcrypt import Bcrypt
from flask_heroku import Heroku
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
md = Markdown(app)

from app.fetcher import *

bf = BackgroundFetcher()
bf.background_scheduler()

from app import routes