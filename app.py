from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def index():
    pokemon = {}
    user = {'username': 'Miguel'}
    posts = [
        {'author': {'username': 'John'}, 'body': 'Beautiful day in Portland!'},
        {'author': {'username': 'Susan'}, 'body': 'The Avengers movie was so cool!'}
    ]
    response = requests.get("https://pokeapi.co/api/v2/pokemon/ditto")
    if response.status_code == 200:
        pokemon =  response.json() # return JSON directly
    else:
        pokemon =  jsonify({"error": "Failed to fetch data"}), response.status_code

    return render_template('index.html', title='Home', user=user, posts=posts, obj=pokemon)

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

# to run locally, run the following command in terminal Python app.py
if __name__ == "__main__":
    app.run(debug=True)