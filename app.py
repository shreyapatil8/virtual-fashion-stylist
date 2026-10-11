# app.py
from flask import Flask, render_template, request, redirect, url_for, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret123"

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['user'] = username
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # (You can later add saving logic to database or file)
        session['user'] = username
        return redirect(url_for('dashboard'))
    return render_template('signup.html')


# ---------- UPDATED DASHBOARD ----------
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    recommendations = []

    if request.method == 'POST':
        gender = request.form.get('gender')
        occasion = request.form.get('occasion')
        style = request.form.get('style')
        color = request.form.get('color')

        # For now, simulate recommendations
        recommendations = [
            f"{gender}_{occasion}_{style}_{color}_1.jpg",
            f"{gender}_{occasion}_{style}_{color}_2.jpg",
            f"{gender}_{occasion}_{style}_{color}_3.jpg"
        ]

    return render_template('dashboard.html',
                           username=session['user'],
                           recommendations=recommendations)
# ----------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
