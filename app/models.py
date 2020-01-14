from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(10), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"User('{self.username}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	subtitle = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


class Fetch(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	repo_title = db.Column(db.String(100), nullable=False)
	repo_time = db.Column(db.String(100), nullable=False)
	blog_title = db.Column(db.String(100), nullable=False)
	blog_url = db.Column(db.String(100), nullable=False)
	comment_url = db.Column(db.String(100), nullable=False)
	comment_time = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Fetch(Github: '{self.repo_title}', '{self.repo_time}'. Blog: '{self.blog_title, self.blog_url}'. Reddit: '{self.comment_url}', '{self.comment_time}')"
