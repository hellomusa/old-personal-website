from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskext_markdown import Markdown

# Get secret key from .txt file
with open('tokens.txt', 'r') as f:
	f.readline()
	SECRET_KEY = f.readline().strip()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
md = Markdown(app)

from app.fetcher import *

bf = BackgroundFetcher()
bf.background_scheduler()

from app import routes