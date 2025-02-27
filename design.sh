#!/bin/bash

# Check if figlet and lolcat are installed
if ! command -v figlet &> /dev/null || ! command -v lolcat &> /dev/null; then
    echo "Please install figlet and lolcat before running this script."
    echo "Install with: sudo apt install figlet lolcat"
    exit 1
fi

# Print "Threat_Eye" in a stylish way
clear
echo "====================================================================" | lolcat
figlet -f slant "Threat_Eye 0.1" | lolcat
echo "=================================================== by ~ Rajat Kundu" | lolcat
