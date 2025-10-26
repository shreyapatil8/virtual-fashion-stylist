from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # required for session management

# ---------- CSV SETUP ----------
if not os.path.exists("users.csv"):
    df = pd.DataFrame(columns=["username", "password", "gender", "style", "body_type", "skin_tone"])
    df.to_csv("users.csv", index=False)

# ---------- ROUTES ----------

@app.route("/", methods=["GET", "POST"])
def login():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        df = pd.read_csv("users.csv")
        user = df[(df["username"] == username) & (df["password"] == password)]
        if not user.empty:
            session["logged_in"] = True
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        gender = request.form["gender"]
        style = request.form["style"]
        body_type = request.form["body_type"]
        skin_tone = request.form["skin_tone"]

        df = pd.read_csv("users.csv")
        if username in df["username"].values:
            flash("Username already exists!", "danger")
        else:
            new_user = pd.DataFrame([[username, password, gender, style, body_type, skin_tone]], columns=df.columns)
            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv("users.csv", index=False)
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please login first!", "warning")
        return redirect(url_for("login"))

    # Load outfits
    data = pd.read_csv("outfits.csv")
    recommendations = None
    if request.method == "POST":
        gender = request.form["gender"]
        occasion = request.form["occasion"]
        color = request.form["color"].strip().lower()
        
        filtered = data[
            (data['gender'].str.lower() == gender.lower()) &
            (data['occasion'].str.lower() == occasion.lower()) &
            (data['color'].str.lower() == color)
        ]
        
        if filtered.empty:
            # Show similar outfits
            filtered = data[
                (data['gender'].str.lower() == gender.lower()) &
                (data['occasion'].str.lower() == occasion.lower())
            ]
            flash("No exact match found. Showing similar outfits.", "info")
        recommendations = filtered.to_dict(orient="records")

    occasions = data['occasion'].unique()
    return render_template("dashboard.html", username=session["username"], occasions=occasions, recommendations=recommendations)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
