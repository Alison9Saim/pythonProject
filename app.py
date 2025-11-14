from flask import Flask, render_template
import gspread
from google.oauth2.service_account import Credentials
import os, json

app = Flask(__name__)

# Define the scope
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Your spreadsheet ID (from the URL)
SPREADSHEET_ID = "12MRrQw-Kl0ktU3IT69_zNxptW-OhauzisEePzS7GFPc"

def get_gspread_client():
    if "GOOGLE_SHEETS_CREDS" in os.environ:
        creds_dict = json.loads(os.environ["GOOGLE_SHEETS_CREDS"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return gspread.authorize(creds)

@app.route("/")
def index():
    client = get_gspread_client()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    values = sheet.get_all_values()

    # Print rows to console (for debugging)
    for row in values:
        print(row)

    return render_template("index.html", title="Home", data=values)

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

# Run locally
if __name__ == "__main__":
    app.run(debug=True)
