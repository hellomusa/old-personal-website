from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Get secret key from .txt file
with open('tokens.txt', 'r') as f:
	f.readline()
	SECRET_KEY = f.readline().strip()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from app import routes