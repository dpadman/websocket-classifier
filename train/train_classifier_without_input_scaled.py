import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import glob
import sys

# Load all labeled CSVs
encrypt=sys.argv[1]
csv_files = glob.glob(f"data-{encrypt}/*_labeled_*.csv")
print(f"csv_files: {len(csv_files)}")
dfs = [pd.read_csv(f) for f in csv_files]
df = pd.concat(dfs, ignore_index=True)

df["label"] = pd.to_numeric(df["label"], errors='coerce')
df = df.dropna(subset=["label"])
df["label"] = df["label"].astype(int)

# Features selected from nDPI CSV
features = ["duration", "c_to_s_pkts", "s_to_c_pkts", "c_to_s_bytes", "s_to_c_bytes"]
X = df[features]
y = df["label"]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

log_clf = LogisticRegression(max_iter=1000)
log_clf.fit(X_train, y_train)

# Evaluation
print("Model performance: Random Forest Classifier")
print(classification_report(y_test, clf.predict(X_test)))

print("Model performance: Logistic Regression Classifier")
print(classification_report(y_test, log_clf.predict(X_test)))

# Save model
joblib.dump(clf, f"model/ai_{encrypt}_classifier.joblib")
print(f"Model saved to model/ai_{encrypt}_classifier.joblib")

joblib.dump(log_clf, f"model/ai_{encrypt}_classifier_logistic.joblib")
print(f"Model saved to model/ai_{encrypt}_classifier_logistic.joblib")
