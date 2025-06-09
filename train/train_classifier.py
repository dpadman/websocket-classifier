import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
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

scaler = MinMaxScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=features)
joblib.dump(scaler, f"model/scaler_{encrypt}.joblib")

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

print("Feature importances:")
for f, imp in zip(features, clf.feature_importances_):
    print(f"{f}: {imp:.4f}")

log_clf = LogisticRegression(max_iter=1000, random_state=42)
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

print("Performing 5-fold stratified cross-validation...")
skf = StratifiedKFold(n_splits = 5, shuffle=True, random_state=42)
scores = cross_val_score(clf, X_scaled, y, cv=skf, scoring='f1_macro')
print(f"Cross-validated F1 scores: {scores}")
print(f"Average F1 score: {scores.mean(): .4f}")

print("Ablation Test: Feature Impact")
for feature in features:
    temp_features = [f for f in features if f != feature]
    X_temp = scaler.fit_transform(df[temp_features])
    X_train_temp, X_test_temp, y_train_temp, y_test_temp = train_test_split(X_temp, y, test_size=0.2, stratify=y, random_state=42)
    temp_clf = RandomForestClassifier(n_estimators=100, random_state=42)
    temp_clf.fit(X_train_temp, y_train_temp)
    temp_score = temp_clf.score(X_test_temp, y_test_temp)
    print(f"Accuracy without {feature}: {temp_score: .4f}")
