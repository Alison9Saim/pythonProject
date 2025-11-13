from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route("/")
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
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
    # from jinja2 import Environment, FileSystemLoader
    # env = Environment(loader=FileSystemLoader('templates'))
    # template = env.get_template('helloName.jinja')
    sites = ['twitter', 'facebook', 'instagram', 'whatsapp']
    return render_template("about.html", sites=sites)


@app.route("/contact/<role>")
def contact(role):
    return render_template("contact.html", person=role)


if __name__ == "__main__":
    app.run(debug=True)



