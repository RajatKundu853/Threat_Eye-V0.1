import os
import time
import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "paste sender email address"
EMAIL_PASSWORD = "paste your app password for the sender email address"
EMAIL_RECEIVER = "paste receiver email address"


# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "paste your bot token here"
TELEGRAM_CHAT_ID = "paste your chat id here"


def log_packet(src_ip, dest_ip, protocol, length, timestamp):
    """Logs captured network packets into the SQLite database with retry logic."""
    for _ in range(5):  # Retry up to 5 times
        try:
            conn = sqlite3.connect("network_logs.db", check_same_thread=False)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO network_logs (src_ip, dest_ip, protocol, length, timestamp) VALUES (?, ?, ?, ?, ?)",
                (src_ip, dest_ip, protocol, length, timestamp),
            )
            conn.commit()
            conn.close()
            break  # Exit loop if successful
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                print("[⚠] Database is locked, retrying...")
                time.sleep(0.5)  # Wait before retrying
            else:
                raise  # Raise other errors


def send_email_alert(ip, mac):
    """Sends an email alert for a detected MITM attack."""
    subject = "🚨 MITM Attack Alert: Suspicious Activity Detected!"
    body = f"""
    Dear User,

    A potential ARP spoofing attack has been detected on your network.
    
    📌 Suspicious Device Details:
    - IP Address: {ip}
    - MAC Address: {mac}
    
    Immediate action is recommended to secure your network.
    
    Stay Safe,
    IoT Security System
    """
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("[✔] Email Alert Sent Successfully!")
    except Exception as e:
        print(f"[✘] Email Alert Failed: {e}")


def send_telegram_alert(ip, mac):
    """Sends a Telegram alert for a detected MITM attack."""
    message = f"⚠️ MITM Attack Detected!\n\n📌 Details:\n- IP: {ip}\n- MAC: {mac}\n\nTake immediate action!"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("[✔] Telegram Alert Sent Successfully!")
    else:
        print(f"[✘] Telegram Alert Failed: {response.json()}")


def log_attack(ip, mac):
    """Logs detected MITM attacks into the SQLite database."""
    conn = sqlite3.connect("network_logs.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS mitm_logs (timestamp TEXT, ip TEXT, mac TEXT)")
    cursor.execute("INSERT INTO mitm_logs VALUES (datetime('now'), ?, ?)", (ip, mac))
    conn.commit()
    conn.close()
    print(f"[✔] Attack Logged: {ip} ({mac})")


def detect_arp_spoofing():
    """Checks the ARP table for duplicate MAC addresses (possible MITM attack)."""
    print("[*] Checking for ARP spoofing...")
    arp_output = os.popen("arp -a").read().split("\n")

    arp_table = {}
    for line in arp_output:
        parts = line.split()
        if len(parts) >= 4:  # Ensure the line contains the necessary fields
            ip = parts[0]
            mac = parts[3]

            if mac in arp_table:
                print(f"[ALERT] Possible ARP Spoofing Detected: {ip} -> {mac}")
                send_telegram_alert(ip, mac)
                send_email_alert(ip, mac)
                log_attack(ip, mac)
            else:
                arp_table[mac] = ip


# Run the ARP spoofing detection every 30 seconds
while True:
    detect_arp_spoofing()
    time.sleep(30)
