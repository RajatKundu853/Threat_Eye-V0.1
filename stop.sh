#!/bin/bash

echo "Stopping Threat_Eye's network detection..."

# Kill only the processes started by run.sh without logging out
pkill -f "python3 network_sniffer.py"
pkill -f "python3 anomaly_detection_and_alert.py"
pkill -f "python3 iot_monitor.py"
pkill -f "python3 mitm_detector.py"
pkill -f "python3 app.py"

# Close all the additional terminals that were opened
pkill -f "x-terminal-emulator"
echo ""
echo "All Threat_Eye services have been stopped."
