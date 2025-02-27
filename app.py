import sqlite3
import time
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Database Connection Helper
def get_db_connection(db_name="network_logs.db"):
    conn = sqlite3.connect(db_name, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")  # Enable WAL mode for concurrent access
    return conn

# User model
class User(UserMixin):
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

# Function to get user from database
def get_user(username):
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return User(*user_data) if user_data else None

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    return User(*user_data) if user_data else None

# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        try:
            conn = get_db_connection("users.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")
    return render_template("signup.html")

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password!", "danger")
    return render_template("login.html")

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Main Dashboard
@app.route("/")
@login_required
def dashboard():
    return render_template("index.html", username=current_user.username)

# Fetch Data from Database
def get_data(query):
    try:
        with get_db_connection() as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Database error: {e}")
        return pd.DataFrame()

# API to fetch network logs
@app.route('/api/logs')
@login_required
def logs():
    data = get_data("SELECT * FROM network_logs ORDER BY timestamp DESC LIMIT 50")
    return jsonify(data.to_dict(orient="records"))

# API for unauthorized IoT devices
@app.route('/api/unauthorized')
@login_required
def unauthorized():
    data = get_data("SELECT * FROM iot_logs WHERE status='UNAUTHORIZED' ORDER BY timestamp DESC")
    records = data.to_dict(orient="records")
    for record in records:
        if record["mac"] is None:
            record["mac"] = "Unknown MAC"
    return jsonify(records)

# API for MITM attack logs
@app.route('/api/mitm')
@login_required
def mitm_attacks():
    data = get_data("SELECT * FROM mitm_logs ORDER BY timestamp DESC")
    return jsonify(data.to_dict(orient="records"))

# API for alerts (unauthorized devices & MITM attacks)
@app.route('/api/alerts')
@login_required
def alerts():
    iot_df = get_data("SELECT * FROM iot_logs WHERE status='UNAUTHORIZED' ORDER BY timestamp DESC LIMIT 5")
    mitm_df = get_data("SELECT * FROM mitm_logs ORDER BY timestamp DESC LIMIT 5")
    alerts_data = {
        "unauthorized_devices": iot_df.to_dict(orient="records"),
        "mitm_attacks": mitm_df.to_dict(orient="records")
    }
    return jsonify(alerts_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
