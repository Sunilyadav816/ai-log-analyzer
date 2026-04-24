import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

# Load data
embeddings = np.load("data/embeddings.npy")
df = pd.read_csv("data/logs.csv")

# Clustering model
model = DBSCAN(eps=0.65, min_samples=2)
labels = model.fit_predict(embeddings)

# Attach labels
df["cluster"] = labels

# Distribution
print("📊 Cluster Distribution:\n")
print(df["cluster"].value_counts())

# Show samples per cluster
print("\n🔍 Cluster Samples:\n")

for cluster_id in sorted(df["cluster"].unique()):
    print(f"\nCluster {cluster_id}:")

    sample_logs = df[df["cluster"] == cluster_id]["logs"].head(5)

    for log in sample_logs:
        print("-", log)

# Separate noise
noise_logs = df[df["cluster"] == -1]["logs"]

print("\n🚨 Noise Logs (Potential Critical Issues):\n")
for log in noise_logs.head(5):
    print("-", log)


    df.to_csv("data/clustered_logs.csv", index=False)