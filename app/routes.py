from flask import render_template, url_for, redirect, request
from app import app, db, bcrypt
from app.forms import LoginForm, PostForm
from app.fetcher import *
from app.models import User, Post
from flask_login import login_user, current_user


def get_post(post_title):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))

	db_titles = [post.title.replace(" ", "-") for post in Post.query.all()]

	if post_title not in db_titles:
		return redirect(url_for('home'))

	post_title = post_title.replace("-", " ")
	post = Post.query.filter_by(title=post_title).first()

	return post


@app.route("/")
def home():
	# Reminder: remove infinite loop, it is not needed (?)
	repo, time = github_fetcher()
	return render_template('home.html', repo_name=repo, time=time)


@app.route("/projects")
def projects():
    return render_template('home.html')


@app.route("/blog")
def blog():
	posts = Post.query.all()
	return render_template('blog.html', posts=posts)


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=False)
			return redirect(url_for('home'))

	return render_template('login.html', form=form)


@app.route("/create", methods=['GET', 'POST'])
def create():
	if not current_user.is_authenticated:
		return redirect(url_for('login'))

	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, subtitle=form.subtitle.data, content=form.content.data)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('home'))

	return render_template('create.html', form=form, legend='Create Post')


@app.route('/post/<post_title>')
def post(post_title):
	post = get_post(post_title)

	return render_template('post.html',post=post)


@app.route('/post/<post_title>/update', methods=['GET', 'POST'])
def update(post_title):
	post = get_post(post_title)
	form = PostForm()

	if form.validate_on_submit():
		post.title = form.title.data
		post.subtitle = form.subtitle.data
		post.content = form.content.data
		db.session.commit()
	elif request.method == 'GET':
		form.title.data = post.title
		form.subtitle.data = post.subtitle
		form.content.data = post.content

	return render_template('create.html', form=form, legend='Update Post')


@app.route('/post/<post_title>/delete', methods=['POST'])
def delete(post_title):
	post = get_post(post_title)
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('home'))