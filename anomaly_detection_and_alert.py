import time
import sqlite3
import pandas as pd
import requests
from sklearn.ensemble import IsolationForest

# Function to log network packets into the database
def log_packet(src_ip, dest_ip, protocol, length, timestamp):
    for _ in range(5):  # Retry up to 5 times
        try:
            conn = sqlite3.connect('network_logs.db', check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS network_logs (src_ip TEXT, dest_ip TEXT, protocol TEXT, length INTEGER, timestamp TEXT)")
            cursor.execute("INSERT INTO network_logs (src_ip, dest_ip, protocol, length, timestamp) VALUES (?, ?, ?, ?, ?)",
                           (src_ip, dest_ip, protocol, length, timestamp))
            conn.commit()
            conn.close()
            break  # Exit loop if successful
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print("[⚠] Database is locked, retrying...")
                time.sleep(0.5)  # Wait before retrying
            else:
                raise  # Raise other errors

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "paste your bot token here"
TELEGRAM_CHAT_ID = "paste your chat id here"

def send_telegram_alert(message):
    """Send an alert message via Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        print("[✔] Telegram Alert Sent Successfully!")
    except requests.exceptions.RequestException as e:
        print(f"[✘] Telegram Alert Failed: {e}")

def detect_anomalies():
    """Fetch network data, run anomaly detection, and check for anomalies."""
    conn = sqlite3.connect('network_logs.db')
    cursor = conn.cursor()

    # Ensure the table exists before reading
    cursor.execute("CREATE TABLE IF NOT EXISTS network_logs (src_ip TEXT, dest_ip TEXT, protocol TEXT, length INTEGER, timestamp TEXT)")
    conn.commit()

    try:
        df = pd.read_sql("SELECT * FROM network_logs", conn)
    except Exception as e:
        print(f"⚠️ Database error: {e}")
        conn.close()
        return

    conn.close()

    if df.empty:
        print("⚠️ No network data found. Waiting for logs...")
        return

    # Train Isolation Forest Model
    X = df[['length']]
    
    # Dynamically adjust contamination rate
    contamination_rate = min(0.05, max(0.01, len(df) / 10000))
    
    model = IsolationForest(contamination=contamination_rate, random_state=42)
    df['anomaly'] = model.fit_predict(X)

    # Identify anomalies
    anomalies = df[df['anomaly'] == -1]

    if not anomalies.empty:
        print("🚨 Anomaly Detected! Sending Telegram Alert...")
        send_telegram_alert("🚨 Anomaly Detected in Network Traffic!")
    else:
        print("✅ No anomalies detected.")

# Run detection continuously every 60 seconds
while True:
    detect_anomalies()
    time.sleep(60)  # Wait 60 seconds before checking again
