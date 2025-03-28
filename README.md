# Threat Eye (v0.1) – Advanced Network Scanner for Kali Linux

## Overview
Threat Eye is a powerful and efficient network scanner designed for Kali Linux, built to enhance network security by detecting anomalies, unauthorized devices, and Man-in-the-Middle (MITM) attacks. It operates in real-time, instantly blocking unauthorized devices and providing instant alerts via Telegram (through the `threat_eye` bot) and email.

## Key Features
- **Network Anomaly Detection** – Monitors and identifies suspicious network activity in real-time.
- **Unauthorized Device Detection & Blocking** – Automatically detects unknown devices connected to the network and blocks them.
- **MITM Attack Detection** – Identifies ongoing MITM attacks and notifies the user immediately.
- **Instant Alerts** – Sends notifications via Telegram bot and email when a security threat is detected.
- **GUI-Based Dashboard** – A user-friendly web dashboard running on localhost, featuring:
  - User Authentication (Sign-up & Login)
  - Real-time Graphs (Packet Size vs. Time)
  - Unauthorized Devices Panel
  - MITM Detection Section
  - Live Notification Panel

## Future Scope in v0.2
- **Forgot Password Feature** – Enable users to recover their accounts easily.
- **OTP Verification** – Secure sign-up and password recovery with OTP-based authentication.
- **Enhanced Detection Mechanisms** – Improve anomaly and attack detection algorithms.
- **Custom Domain & Port Forwarding** – Allow remote access with proper configurations.
- **HTTPS & Cloudflare Protection** – Secure the dashboard against DDoS attacks and unauthorized access.

## Installation
```bash
sudo su
apt update && apt upgrade -y
apt autoremove -y
git clone https://github.com/RajatKundu853/Threat_Eye-V0.1
cd Threat_Eye-V0.1
chmod +x *
./setup.sh
reboot  # (optional)
```

## Bot & Mail Setup
Edit the following files to add your bot token, chat ID, and email details:
- **anomaly_detection_and_alert.py** (Line 27 & 28)
- **iot_monitor.py** (Line 36 & 37 for Telegram, Line 15, 16 & 17 for email)
- **mitm_detector.py** (Line 17 & 18 for Telegram, Line 12, 13 & 14 for email)

## Whitelist Devices
```bash
sudo su
./whitelist.sh
```

## Run Threat Eye
```bash
sudo su
./threat_eye.sh
```

## Hard Reset (Database Operations)
⚠️ **Warning:** Don't use if you don't know how to handle the database. This may break Threat Eye.
```bash
sqlite3 <database_name>  # Open & select database
.tables  # Show all tables
.headers ON  # Show column names
.mode column  # Show data in columns
SELECT * FROM <table_name>;  # Show all data from a table
DELETE FROM <table_name>;  # Delete all data from table
DELETE FROM sqlite_sequence WHERE name='<table_name>';  # Reset auto-increment of primary key
VACUUM;  # Optimize database space
.exit  # Exit from database
```

## Admin Use Only
⚠️ **Warning:** Never execute these unless absolutely necessary.
```sql
INSERT INTO iot_logs (timestamp, ip, mac, status) VALUES ('2025-02-27 14:30:00', '192.168.1.10', 'AA:BB:CC:DD:EE:FF', 'UNAUTHORIZED');

CREATE TABLE IF NOT EXISTS mitm_logs (timestamp TEXT, ip TEXT, mac TEXT);

INSERT INTO mitm_logs VALUES ('2025-02-27 14:30:00', '192.168.1.10', 'AA:BB:CC:DD:EE:FF');
```

## License
[MIT License](LICENSE)

## Author
**Rajat Kundu**

For contributions, issues, or feature requests, open an issue on GitHub or contact me directly!
