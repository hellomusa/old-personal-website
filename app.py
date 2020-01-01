from flask import Flask, render_template, url_for, redirect
from fetcher import *
from forms import LoginForm

app = Flask(__name__)

# Get secret key from .txt file
with open('tokens.txt', 'r') as f:
	f.readline()
	SECRET_KEY = f.readline().strip()

app.config['SECRET_KEY'] = SECRET_KEY


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

if __name__ == '__main__':
    app.run(debug=True)