from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

# Load cleaned logs
df = pd.read_csv("data/logs.csv")
logs = df["clean_logs"].tolist()

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert logs → vectors
embeddings = model.encode(logs)

# Print shape
print("Shape:", len(embeddings), len(embeddings[0]))

# Save embeddings
np.save("data/embeddings.npy", embeddings)

print("Saved embeddings!")