import os
import time
import sqlite3
import subprocess
import re
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "paste sender email address"
EMAIL_PASSWORD = "paste your app password for the sender email address"
EMAIL_RECEIVER = "paste receiver email address"

def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"[✔] Email Alert Sent Successfully! Subject: {subject}")
    except Exception as e:
        print(f"[✘] Email Alert Failed: {e}")

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "paste your bot token here"
TELEGRAM_CHAT_ID = "paste your chat id here"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("[✔] Telegram Alert Sent Successfully!")
    else:
        print(f"[✘] Telegram Alert Failed: {response.json()}")

# Function to block unauthorized devices
def block_device(ip):
    print(f"[BLOCKING] Unauthorized device detected: {ip}")
    os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
    os.system(f"sudo iptables -A FORWARD -s {ip} -j DROP")
    print(f"[✔] Device {ip} has been successfully blocked!")

# Load whitelist (convert to lowercase for case consistency)
def load_whitelist():
    try:
        with open("whitelist.txt", "r") as file:
            return set(line.strip().lower() for line in file if line.strip())  # Using a set for fast lookup
    except FileNotFoundError:
        print("whitelist.txt not found! Creating an empty whitelist.")
        open("whitelist.txt", "w").close()
        return set()

WHITELIST = load_whitelist()

# Function to scan network and get connected devices
def scan_network():
    devices = []
    try:
        output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
        for line in output.split("\n"):
            match = re.search(r"\((\d+\.\d+\.\d+\.\d+)\)\s+.*?([a-fA-F0-9:-]{17})", line)
            if match:
                ip_address = match.group(1)
                mac_address = match.group(2).lower()  # Convert MAC to lowercase
                devices.append((ip_address, mac_address))
    except Exception as e:
        print(f"Error scanning network: {e}")
    return devices

# Function to check for unauthorized devices
def check_for_unauthorized_devices():
    print("[INFO] Device monitoring in progress...\n")
    detected_devices = scan_network()
    
    # Connect to database
    conn = sqlite3.connect("network_logs.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS iot_logs (timestamp TEXT, ip TEXT, mac TEXT, status TEXT)")

    for ip, mac in detected_devices:
        # Debugging output
        print(f"Fetched IP: {ip}, Fetched MAC: {mac}")

        # Generate dynamic timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Determine device status
        status = "AUTHORIZED" if mac in WHITELIST else "UNAUTHORIZED"

        # Debugging output before inserting into DB
        print(f"Timestamp: {timestamp}, IP: {ip}, MAC: {mac}, Status: {status}")

        # Insert into database
        cursor.execute("INSERT INTO iot_logs (timestamp, ip, mac, status) VALUES (?, ?, ?, ?)",
                       (timestamp, ip, mac, status))

        # If device is unauthorized, send alerts and block it
        if status == "UNAUTHORIZED":
            print(f"[ALERT] Unauthorized IoT device detected: {ip} ({mac})")
            block_device(ip)
            send_telegram_alert(f"🚨 Unauthorized IoT Device Detected: {ip} ({mac})")
            email_subject = "[ALERT] 🚨 Unauthorized IoT Device Detected!"
            email_body = f"An unauthorized device has been detected on the network.\n\nIP Address: {ip}\nMAC Address: {mac}\n\nThe device has been blocked.\nIf you trust it, manually add the MAC address to the whitelist."
            send_email_alert(email_subject, email_body)

    # Commit and close database
    conn.commit()
    conn.close()

# Run the monitoring script every 60 seconds
while True:
    check_for_unauthorized_devices()
    time.sleep(60)
