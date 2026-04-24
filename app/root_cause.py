import pandas as pd
from collections import Counter

# Load clustered logs
df = pd.read_csv("data/clustered_logs.csv")

def extract_keywords(logs):
    words = []
    for log in logs:
        words.extend(log.lower().split())
    return Counter(words)
def get_root_cause(logs):
    word_freq = extract_keywords(logs)
    keywords = set(word_freq.keys())

    # HIGH PRIORITY (critical issues first)

    if {"security", "unauthorized"} & keywords:
        return "Security Breach"

    elif {"kernel", "crash"} & keywords:
        return "System Crash"

    elif {"disk"} & keywords:
        return "Disk Failure"

    # MEDIUM PRIORITY

    elif {"db", "database", "connection"} & keywords:
        return "Database Connectivity Issue"

    elif {"auth", "authentication", "credential"} & keywords:
        return "Authentication Failure"

    # LOW PRIORITY

    elif {"memory"} & keywords:
        return "Memory Usage Issue"

    elif {"payment", "transaction"} & keywords:
        return "Payment System Activity"

    elif {"login", "logged"} & keywords and "error" not in keywords:
        return "Successful Login Activity"

    else:
        return "Unknown Issue"

# Process clusters
clusters = sorted(df["cluster"].unique())



label_map = {}

for c in clusters:

    if c == -1:
        logs = df[df["cluster"] == -1]["logs"].tolist()
        keywords = extract_keywords(logs)

        issues = []

        if "security" in keywords:
            issues.append("Security Breach")
        if "kernel" in keywords or "crash" in keywords:
            issues.append("System Crash")
        if "memory" in keywords:
            issues.append("Memory Issue")

        label = f"Critical Issues: {', '.join(issues)}"
    else:
        logs = df[df["cluster"] == c]["logs"].tolist()
        label = get_root_cause(logs)

    if label not in label_map:
        label_map[label] = []

    label_map[label].extend(logs)

# 🔥 Final clean output
print("\n🧠 Final Issue Summary:\n")

for label, logs in label_map.items():
    print(f"{label} → {len(logs)} logs")