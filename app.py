from flask import Flask, render_template, redirect, url_for, session, request
import gspread
from google.oauth2.service_account import Credentials
import os, json, random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

@app.context_processor
def inject_now():
    return {'current_year': datetime.now().year}


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

    # Pick a random row (skip header)
    random_idx = random.randint(0, len(rows)-1)
    row = rows[random_idx]

    # Actual sheet row number = header row (1) + offset
    sheet_row_number = random_idx + 2

    question = row[0]
    option_a = row[1]
    option_b = row[2]

    # Initialize points if not set
    if "points" not in session:
        session["points"] = 0

    return render_template(
        "index.html",
        question=question,
        option_a=option_a,
        option_b=option_b,
        row_index=sheet_row_number,   # ✅ pass row_index here
        points=session["points"]
    )

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

    if selected_votes >= other_votes:
        session["points"] = session.get("points", 0) + 1
        return redirect(url_for("index"))
    else:
        # Capture the score before resetting
        previous_points = session.get("points", 0)
        session["points"] = 0

        # Fetch funny messages from second sheet
        messages_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Lose Messages")
        messages = messages_sheet.col_values(1)
        loss_message = random.choice(messages) if messages else "Better luck next time!"

        # Pass previous_points directly to template
        return render_template("try_again.html",
                               points=previous_points,
                               loss_message=loss_message)



@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/home")
def home():
    return render_template("home.html")



@app.route("/blog")
def blog():
    return render_template("blog/index.html")

@app.route("/blog/1")
def blog_post1():
    return render_template("blog/post1.html")

@app.route("/blog/2")
def blog_post2():
    return render_template("blog/post2.html")

@app.route("/blog/3")
def blog_post3():
    return render_template("blog/post3.html")

@app.route("/blog/4")
def blog_post4():
    return render_template("blog/post4.html")

@app.route("/blog/5")
def blog_post5():
    return render_template("blog/post5.html")

@app.route("/blog/funny")
def blog_funny():
    return render_template("blog/funny.html")

@app.route("/blog/psychology")
def blog_psychology():
    return render_template("blog/psychology.html")

@app.route("/blog/history")
def blog_history():
    return render_template("blog/history.html")


@app.route("/highscores")
def highscores():
    client = get_gspread_client()
    record_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Highscores")

    # Get all rows as list of dicts (first row must be headers: Name, Points, Timestamp)
    records = record_sheet.get_all_records()

    return render_template("highscore.html", highscores=records)



@app.route("/try_again")
def try_again():
    # Use the points stored in session
    points = session.get("points", 0)
    return render_template("try_again.html", points=points)


@app.route("/submit_highscore", methods=["POST"])
def submit_highscore():
    name = request.form.get("name")
    points = request.form.get("points")

    if not name or not points:
        return "Invalid submission", 400

    try:
        points = int(points)
    except ValueError:
        points = 0

    client = get_gspread_client()
    record_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Highscores")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_sheet.append_row([name, points, timestamp])

    return redirect(url_for("highscores"))



# Run locally
if __name__ == "__main__":
    app.run(debug=True)
