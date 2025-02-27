# Threat Eye (v0.1) – Advanced Network Scanner for Kali Linux
# Overview

Threat Eye is a powerful and efficient network scanner designed for Kali Linux, built to enhance network security by detecting anomalies, unauthorized devices, and Man-in-the-Middle (MITM) attacks. It operates in real-time, instantly blocking unauthorized devices and providing instant alerts via Telegram (through the "threat_eye" bot) and email.

# Key Features

**Network Anomaly Detection  –** Monitors and identifies suspicious network activity in real-time.

**Unauthorized Device Detection & Blocking –** Automatically detects unknown devices connected to the network and blocks them.

**MITM Attack Detection –** Identifies ongoing MITM attacks and notifies the user immediately.

**Instant Alerts –** Sends notifications via Telegram bot and email when a security threat is detected.

**GUI-Based Dashboard –** A user-friendly web dashboard running on localhost, featuring:

**User Authentication (Sign-up & Login)**

**Real-time Graphs (Packet Size vs. Time)**

**Unauthorized Devices Panel**

**MITM Detection Section**

**Live Notification Panel**

# Future Scope in V_0.2

**Forgot Password Feature –** Enable users to recover their accounts easily.

**OTP Verification –** Secure sign-up and password recovery with OTP-based authentication.

**Enhanced Detection Mechanisms –** Improve anomaly and attack detection algorithms.

**Custom Domain & Port Forwarding –** Allow remote access with proper configurations.

**HTTPS & Cloudflare Protection –** Secure the dashboard against DDoS attacks and unauthorized access.

# Installation

sudo su

apt update && apt upgrade -y

apt autoremove -y

git clone https://github.com/RajatKundu853/Threat_Eye-V0.1

cd Threat_Eye-V0.1

chmod +x *

./setup.sh

reboot (optional)

# Bot & Mail Setup

Add your Telegram bot token & chat ID in line number 27 & 28 of anomaly_detection_and_alert.py

Add your Telegram bot token & chat ID in line number 36 & 37 of iot_monitor.py

Add sender mail address, app password for the sender email address & receiver mail address in line number 15, 16 & 17 of iot_monitor.py

Add your Telegram bot token & chat ID in line number 17 & 18 of mitm_detector.py

Add sender mail address, app password for the sender email address & receiver mail address in line number 12, 13 & 14 of mitm_detector.py

# Whitelist Devices

sudo su

./whitelist.sh

# Run Threat Eye

sudo su

./threat_eye.sh

# Hard Reset (Database Operations)

**⚠️ Warning: Don't use if you don't know how to handle the database. This may break Threat Eye.**

sqlite3 <database_name>  (open & select database)

.tables  (show all tables)

.headers ON  (for a readable format - show column names)

.mode column  (for a readable format - show data in columns)

SELECT * FROM <table_name>;  (show all data from the table)

DELETE FROM <table_name>;  (delete all data from table)

DELETE FROM sqlite_sequence WHERE name='<table_name>';  (reset auto-increment of primary key)

VACUUM;  (optimize database space)

.exit  (exit from database)

# Admin Use Only

**⚠️ Warning: Never execute these unless absolutely necessary.**

INSERT INTO iot_logs (timestamp, ip, mac, status) VALUES ('2025-02-27 14:30:00', '192.168.1.10', 'AA:BB:CC:DD:EE:FF', 'UNAUTHORIZED');

CREATE TABLE IF NOT EXISTS mitm_logs (timestamp TEXT, ip TEXT, mac TEXT);

INSERT INTO mitm_logs VALUES ('2025-02-27 14:30:00', '192.168.1.10', 'AA:BB:CC:DD:EE:FF');



