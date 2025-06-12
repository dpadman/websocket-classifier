import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Path to nDPI CSV from command-line
csv_path = sys.argv[1]

# Load nDPI CSV
df = pd.read_csv(csv_path, sep='|')
df.columns = df.columns.str.strip()
df = df[(df["src_port"].isin([80, 443, 8765])) | (df["dst_port"].isin([80, 443, 8765]))]

# Use only flows with TCP/WebSocket-like behavior (optionally add filters)
# Select feature columns: adjust these based on your actual nDPI CSV structure
# Map to shorter names for consistency

print("Before rename:", df.columns.tolist())
df = df.rename(columns={
    "duration": "duration",
    "c_to_s_pkts": "packets_in",
    "s_to_c_pkts": "packets_out",
    "c_to_s_bytes": "bytes_in",
    "s_to_c_bytes": "bytes_out"
})
print("After rename:", df.columns.tolist())

X = df[["duration", "packets_in", "packets_out", "bytes_in", "bytes_out"]]

# Simulated training
training_data = {
    "duration": [1.2, 3.4, 0.8, 4.5, 2.0, 1.1, 3.0, 0.9],
    "packets_in": [10, 50, 8, 60, 25, 12, 55, 9],
    "packets_out": [12, 45, 7, 58, 20, 10, 50, 11],
    "bytes_in": [1200, 5200, 800, 6100, 2100, 1100, 5000, 900],
    "bytes_out": [1300, 5000, 750, 6000, 2000, 1000, 4800, 1000],
    "label": [0, 1, 0, 1, 1, 0, 1, 0]  # 1 = AI WebSocket
}
train_df = pd.DataFrame(training_data)
X_train = train_df[["duration", "packets_in", "packets_out", "bytes_in", "bytes_out"]]
y_train = train_df["label"]

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Predict AI WebSocket or not
predictions = model.predict(X)
for i, pred in enumerate(predictions):
    print(f"Flow {i+1}: {'AI WebSocket' if pred == 1 else 'Regular WebSocket'}")
