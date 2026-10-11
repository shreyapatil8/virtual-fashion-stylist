from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ----------------- CSV SETUP -----------------
if not os.path.exists("users.csv"):
    df = pd.DataFrame(columns=["username", "password", "gender", "style", "body_type", "skin_tone"])
    df.to_csv("users.csv", index=False)

# ----------------- LOGIN -----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        
        try:
            df = pd.read_csv("users.csv")
            user = df[(df['username'] == username) & (df['password'] == password)]
            if not user.empty:
                session['logged_in'] = True
                session['username'] = username
                flash(f"Welcome back, {username}!", "success")
                return redirect(url_for('dashboard'))  # ✅ redirect to dashboard
            else:
                flash("Invalid username or password.", "danger")
        except Exception as e:
            flash("Error reading users.csv", "danger")
    return render_template("login.html")


# ----------------- SIGNUP -----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        gender = request.form["gender"]
        style = request.form["style"]
        body_type = request.form["body_type"]
        skin_tone = request.form["skin_tone"]

        df = pd.read_csv("users.csv")
        if username in df['username'].values:
            flash("Username already exists!", "warning")
        else:
            new_user = pd.DataFrame([[username, password, gender, style, body_type, skin_tone]], columns=df.columns)
            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv("users.csv", index=False)
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))  # redirect to login page

    return render_template("signup.html")


# ----------------- LOGOUT -----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))


from app import app  # import Flask app and dashboard routes

if __name__ == "__main__":
    app.run(debug=True)
