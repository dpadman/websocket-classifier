import joblib
import pandas as pd

# Load trained model
clf = joblib.load("model/ai_ws_classifier.joblib")

# Sample flow data (e.g. from nDPI CSV)
features = ["duration", "c_to_s_pkts", "s_to_c_pkts", "c_to_s_bytes", "s_to_c_bytes"]
flow_df = pd.read_csv("data/recent_ws_flows.csv")
X = flow_df[features]

# Predict
predictions = clf.predict(X)
flow_df["prediction"] = predictions
print(flow_df[["src_ip", "dst_ip", "prediction"]])
