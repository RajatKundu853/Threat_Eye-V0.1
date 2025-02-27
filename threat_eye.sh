#!/bin/bash

./design.sh
echo ""
echo "----------------------------------------------------------------------"
echo "To stop Threat_Eye's network detection use: ./stop.sh"
echo "----------------------------------------------------------------------"
echo ""

export QT_LOGGING_RULES="*.debug=false"  # it disable the logs showing in terminal
# export QT_QPA_PLATFORMTHEME=gtk2       # you can enable this line by removing the # to use gtk2 theme

# Open a new terminal and run network_sniffer script
x-terminal-emulator -e "bash -c 'sudo python3 network_sniffer.py; exec bash'" &
sleep 12

# Open a new terminal and run anomaly detection script
x-terminal-emulator -e "bash -c 'python3 anomaly_detection_and_alert.py; exec bash'" &

# Wait for 3 seconds
sleep 3

# Open a new terminal and run IoT monitor script
x-terminal-emulator -e "bash -c 'python3 iot_monitor.py; exec bash'" &

# Wait for 3 seconds
sleep 3

# Open a new terminal and run MITM detector script
x-terminal-emulator -e "bash -c 'python3 mitm_detector.py; exec bash'" &

# Wait for 3 seconds
sleep 3

# Open a new terminal and run the web app
x-terminal-emulator -e "bash -c 'python3 app.py; exec bash'" &

# Wait for 5 seconds to ensure services start
sleep 3

# Open the web app in the default browser
xdg-open "http://127.0.0.1:5000"
