import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle

# -------------------------------
# 📥 Load dataset
# -------------------------------
df = pd.read_csv("data/labeled_logs.csv")

logs = df["log"].tolist()
labels = df["label"].tolist()

print(f"Total samples: {len(logs)}")

# -------------------------------
# 🔀 Train-Test Split (FIRST)
# -------------------------------
X_train_logs, X_test_logs, y_train, y_test = train_test_split(
    logs, labels, test_size=0.2, random_state=42
)

# -------------------------------
# 🧠 Load embedding model
# -------------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# encode separately (IMPORTANT)
X_train = model.encode(X_train_logs)
X_test = model.encode(X_test_logs)

# -------------------------------
# 🤖 Train ML model
# -------------------------------
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(X_train, y_train)

# -------------------------------
# 📊 REAL Evaluation
# -------------------------------
y_pred = clf.predict(X_test)

print("\n📊 REAL Evaluation:\n")
print(classification_report(y_test, y_pred))

# -------------------------------
# 💾 Save model
# -------------------------------
with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("\n✅ Model saved as model.pkl")