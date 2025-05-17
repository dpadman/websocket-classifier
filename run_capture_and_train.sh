#!/bin/bash

# Usage: ./run_capture_and_train.sh <interface> <label> <duration_sec> <ws/wss>
# Example: ./run_capture_and_train.sh eth0 1 30 wss

if [[ $# -ne 4 ]]; then
	echo "./run_capture_and_train.sh <interface> <label> <duration_sec> <ws/wss>"
	exit 1
fi

INTERFACE=$1
LABEL=$2
DURATION=${3:-30}
ENCRYPT=$4 # encrypted is wss, non-encrypted ws
TIMESTAMP=$(date +%s)
CSV_FILE="data-${ENCRYPT}/${ENCRYPT}_capture_${TIMESTAMP}.csv"

echo "[*] Capturing traffic on $INTERFACE for $DURATION seconds..."
sudo nDPI/example/ndpiReader -i "$INTERFACE" -C "$CSV_FILE" &

PID=$!
sleep "$DURATION"
kill -2 $PID
sleep 1

echo "[*] Labeling traffic as $LABEL (AI=1 / non-AI=0)..."
python3 train/label_data.py "$CSV_FILE" "$LABEL"

echo "[*] Training classifier on all labeled data..."
python3 train/train_classifier.py "$ENCRYPT"

echo "[*] Done."


