from flask import Flask, render_template
from fetcher import *

app = Flask(__name__)


@app.route("/")
def home():
	repo, time = github_fetcher()
	return render_template('home.html', repo_name=repo, time=time)


@app.route("/projects")
def projects():
    return render_template('home.html')

@app.route("/experiences")
def experiences():
    return render_template('home.html')

@app.route("/writing")
def writing():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)