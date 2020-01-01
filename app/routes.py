from flask import render_template, url_for, redirect
from app import app
from app.forms import LoginForm
from app.fetcher import *
from app.models import User, Post

@app.route("/")
def home():
	repo, time = github_fetcher()
	return render_template('home.html', repo_name=repo, time=time)


@app.route("/projects")
def projects():
    return render_template('home.html')


@app.route("/blog")
def blog():
    return render_template('blog.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		# Placeholder login info
		if form.username.data == 'musaali' and form.password.data == 'admin':
			return redirect(url_for('home'))
	return render_template('login.html', form=form)