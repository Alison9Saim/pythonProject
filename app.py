from flask import Flask, render_template, redirect, url_for, session
import gspread
from google.oauth2.service_account import Credentials
import os, json, random

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

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

    headers = values[0]
    rows = values[1:]

    random_idx = random.randint(0, len(rows)-1)
    row = rows[random_idx]
    sheet_row_number = random_idx + 2  # account for header row

    question = row[0]
    option_a = row[1]
    option_b = row[2]
    votes_a = int(row[3]) if row[3] else 0
    votes_b = int(row[4]) if row[4] else 0

    # initialize points if not set
    if "points" not in session:
        session["points"] = 0

    return render_template("index.html",
                           question=question,
                           option_a=option_a,
                           option_b=option_b,
                           row_index=sheet_row_number,
                           votes_a=votes_a,
                           votes_b=votes_b,
                           points=session["points"])

@app.route("/vote/<int:row_index>/<choice>")
def vote(row_index, choice):
    client = get_gspread_client()
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1

    votes_a = int(sheet.acell(f"D{row_index}").value or 0)
    votes_b = int(sheet.acell(f"E{row_index}").value or 0)

    if choice == "A":
        sheet.update_acell(f"D{row_index}", votes_a + 1)
        selected_votes = votes_a + 1
        other_votes = votes_b
    elif choice == "B":
        sheet.update_acell(f"E{row_index}", votes_b + 1)
        selected_votes = votes_b + 1
        other_votes = votes_a
    else:
        return redirect(url_for("index"))

    # Decide points outcome
    if selected_votes >= other_votes:
        session["points"] = session.get("points", 0) + 1
        return redirect(url_for("index"))
    else:
        # Save score before reset
        previous_points = session.get("points", 0)
        session["points"] = 0
        return render_template("try_again.html", previous_points=previous_points, points=session["points"])


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
