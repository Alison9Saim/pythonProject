from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route("/")
def index():
    user = {'username': 'Miguel'}
    posts = [
        {'author': {'username': 'John'}, 'body': 'Beautiful day in Portland!'},
        {'author': {'username': 'Susan'}, 'body': 'The Avengers movie was so cool!'}
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("about.html", sites=sites)

@app.route("/contact/<role>")
def contact(role):
    return render_template("contact.html", person=role)
