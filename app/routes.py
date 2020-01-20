from flask import render_template, url_for, redirect, request, Markup
from flask_login import login_user, current_user, login_required
from markdown import markdown
from app import app, db, bcrypt
from .fetcher import *
from .forms import LoginForm, PostForm
from .models import User, Post, Fetch


@app.route("/")
def home():
	repo_name, repo_time, blog_name, blog_url, comment_url, comment_time = db_to_list()
	#repo_name, repo_time, blog_name, blog_url, comment_url, comment_time = [1,2,3,4,5,6]
	return render_template('home.html', 
							repo_name=repo_name, 
							repo_time=repo_time, 
							blog_name=blog_name,
							blog_url=blog_url,
							comment_url=comment_url,
							comment_time=comment_time)


@app.route("/blog")
def blog():
	posts = Post.query.all()
	return render_template('blog.html', posts=posts)


@app.route('/blog/<post_title>')
def post(post_title):
	post = get_post(post_title)

	return render_template('post.html',post=post)


@app.route("/blog/create", methods=['GET', 'POST'])
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


@app.route('/blog/<post_title>/update', methods=['GET', 'POST'])
def update(post_title):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))

	form = PostForm()
	post = get_post(post_title)

	if form.validate_on_submit():
		post.title = form.title.data
		post.subtitle = form.subtitle.data
		post.content = form.content.data
		db.session.commit()
		return redirect(url_for('home'))
	elif request.method == 'GET':
		form.title.data = post.title
		form.subtitle.data = post.subtitle
		form.content.data = post.content

	return render_template('create.html', form=form, legend='Update Post')


@app.route('/blog/<post_title>/delete', methods=['GET', 'POST'])
def delete(post_title):
	if not current_user.is_authenticated:
		return redirect(url_for('login'))

	post = get_post(post_title)
	db.session.delete(post)
	db.session.commit()

	return redirect(url_for('home'))


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


@app.template_filter("markdown")
def render_markdown(markdown_text):
	return Markup(markdown(markdown_text))