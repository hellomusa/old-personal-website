from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


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