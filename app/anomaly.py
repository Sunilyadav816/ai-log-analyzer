import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Load embeddings
embeddings = np.load("data/embeddings.npy")

# Load original logs
df = pd.read_csv("data/logs.csv")

# Train model
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(embeddings)

# Predict
preds = model.predict(embeddings)

# Count
total = len(preds)
anomalies = sum(preds == -1)
normal = sum(preds == 1)

print("Total logs:", total)
print("Normal logs:", normal)
print("Anomalies:", anomalies)

# Show actual anomaly logs
print("\n🔴 Sample Anomaly Logs:")
count = 0
for i, p in enumerate(preds):
    if p == -1:
        print("-", df["logs"][i])
        count += 1
    if count == 5:
        break