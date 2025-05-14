#!/bin/bash

# Network interface to monitor
INTERFACE="enX0"

# Output CSV from nDPI
NDPI_CSV="ndpi_flows.csv"

# Python classifier script
PY_SCRIPT="ai_ws_classifier.py"

echo "[*] Capturing traffic with nDPI on interface $INTERFACE..."

# Capture for 30 seconds and export to CSV
sudo ./nDPI/example/ndpiReader -i $INTERFACE -C $NDPI_CSV &

PID=$!
sleep 60
kill -2 $PID
sleep 2

echo "[*] Traffic capture complete. Saved to $NDPI_CSV"

# Optional: Remove header or filter flows as needed

echo "[*] Running AI classifier..."
python3 $PY_SCRIPT $NDPI_CSV
