import pandas as pd
import sys

if len(sys.argv) < 3:
    print("Usage: python label_data.py <input.csv> <label (0 or 1)>")
    sys.exit(1)

input_csv = sys.argv[1]
label = int(sys.argv[2])

df = pd.read_csv(input_csv, sep='|')
df = df[(df["src_port"].isin([80, 443, 8765])) | (df["dst_port"].isin([80, 443, 8765]))]
df['label'] = label

df.to_csv(input_csv.replace(".csv", f"_labeled_{label}.csv"), index=False)
print(f"Labeled data saved as {input_csv.replace('.csv', f'_labeled_{label}.csv')}")
