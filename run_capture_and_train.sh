#!/bin/bash

# Usage: ./run_capture_and_train.sh <interface> <label> <duration_sec>
# Example: ./run_capture_and_train.sh eth0 1 30

INTERFACE=$1
LABEL=$2
DURATION=${3:-30}
TIMESTAMP=$(date +%s)
CSV_FILE="data/ws_capture_${TIMESTAMP}.csv"

echo "[*] Capturing traffic on $INTERFACE for $DURATION seconds..."
sudo nDPI/example/ndpiReader -i "$INTERFACE" -C "$CSV_FILE" &

PID=$!
sleep "$DURATION"
kill -2 $PID
sleep 1

echo "[*] Labeling traffic as $LABEL (AI=1 / non-AI=0)..."
python3 train/label_data.py "$CSV_FILE" "$LABEL"

echo "[*] Training classifier on all labeled data..."
python3 train/train_classifier.py

echo "[*] Done."


