#!/bin/bash

echo "WE BUILD & VERIFY YOUR SYSTEM TO RUN THREAT_EYE SMOOTHLY"
echo "  "
echo "  "
echo "PLEASE WAIT WHILE INSTALL REQUIRED PACKAGES/TOOLS,LIBRARIES & DEPENDENCIES...... "
echo "  "
echo "  "
sleep 10

set -e  # Exit on any error

# Function to handle errors
error_exit() {
    echo "❌ Error occurred at Step $1"
    exit 1
}

# Step 1: Update & Upgrade
echo "🔄 Step 1: Updating & Upgrading Your System..."
sudo apt update && sudo apt upgrade -y || error_exit 1

echo "  "
echo "  "
sleep 2

# Step 2: Install necessary packages
echo "📦 Step 2: Installing required packages..."
sudo apt install qt6ct wireshark tshark sqlite3 python3-pip python3-flask arp-scan nmap arpwatch tcpdump nginx certbot python3-certbot-nginx figlet lolcat -y || error_exit 2

echo "  "
echo "  "
sleep 2

# Step 3: Install Python dependencies
echo "🐍 Step 3: Installing Python libraries..."
sudo apt install -y \
    python3-scapy python3-pandas python3-numpy python3-sklearn \
    python3-flask python3-flask-login python3-flask-sqlalchemy \
    python3-flask-cors python3-matplotlib python3-requests python3-werkzeug || error_exit 3
    
echo "  "
echo "  "
sleep 2

# Step 4: Add user to Wireshark group
echo "👤 Step 4: Adding user to Wireshark group..."
sudo usermod -aG wireshark $USER || error_exit 4

echo "  "
echo "  "
sleep 2

# Step 5: Apply group changes
echo "🔄 Just another one minutes >>>> Applying group changes..."
echo "  "
echo "  "
sleep 2

# Confirmation message after successful completion
echo "✅ All steps completed successfully!"
echo "  "
echo "  "
echo "🎉 Your system is now set up and ready for THREAT_EYE ."
echo "  "
echo " Now you can reboot the system for better performance. "
newgrp wireshark || error_exit 5

