from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.cluster import DBSCAN
from sentence_transformers import SentenceTransformer
import pickle
import re

from app.root_cause import get_root_cause
from app.preprocess import preprocess_logs

app = FastAPI()
model = SentenceTransformer("all-MiniLM-L6-v2")

# -------------------------------
# 🔥 LOAD ML MODEL
# -------------------------------
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)


class LogRequest(BaseModel):
    logs: list[str]


# -------------------------------
# ✅ SOLUTION
# -------------------------------
def get_solution(issue):
    return {
        "Security Breach": "Immediately block IP, reset credentials, and review access logs.",
        "System Crash": "Restart system, check system logs, and monitor CPU/memory usage.",
        "Database Connectivity Issue": "Check DB server status, connection string, and network.",
        "Successful Login Activity": "No action needed.",
        "Authentication Failure": "Verify credentials and monitor repeated failed attempts.",
        "Payment System Activity": "Verify transactions and check payment gateway logs.",
        "Memory Issue": "Check memory usage and restart affected services.",
        "Web Request Activity": "Normal HTTP request, no action needed.",
        "Page Not Found": "Check URL or routing configuration.",
        "Server Error": "Check backend services and server logs.",
        "Disk Failure": "Check disk health and replace if needed.",
        "Other Critical Issue": "Investigate logs manually."
    }.get(issue, "No solution available.")


# -------------------------------
# ✅ SEVERITY
# -------------------------------
def get_severity(issue):
    return {
        "Security Breach": "High",
        "System Crash": "High",
        "Memory Issue": "High",
        "Server Error": "High",
        "Disk Failure": "High",

        "Database Connectivity Issue": "Medium",
        "Authentication Failure": "Medium",
        "Payment System Activity": "Medium",
        "Page Not Found": "Medium",

        "Successful Login Activity": "Low",
        "Web Request Activity": "Low",
        "Other Critical Issue": "Medium"
    }.get(issue, "Low")


# -------------------------------
# 🔥 SMART RULE ENGINE (FINAL FIX)
# -------------------------------
def rule_based_override(log):

    log_lower = log.lower()

    # 🔴 SECURITY (TOP PRIORITY)
    if (
        "unauthorized" in log_lower
        or "breach" in log_lower
        or "suspicious" in log_lower
        or "attack" in log_lower
    ):
        return "Security Breach"

    # 🔐 AUTH (SMART CONTEXT)
    if "login" in log_lower or "auth" in log_lower:

        # 🔥 failure patterns
        if any(word in log_lower for word in [
            "failed", "invalid", "retry", "retrying",
            "timeout", "error", "denied"
        ]):
            return "Authentication Failure"

        # 🔥 suspicious behavior
        if "multiple attempts" in log_lower:
            return "Authentication Failure"

        return "Successful Login Activity"

    # 🌐 WEB LOGS
    if re.search(r'(get|post|put|delete).*http', log_lower):

        if "500" in log:
            return "Server Error"
        elif "404" in log:
            return "Page Not Found"
        elif "200" in log:
            return "Web Request Activity"

        return "Web Request Activity"

    # 💾 DATABASE
    if any(word in log_lower for word in ["db", "database", "connection"]):
        return "Database Connectivity Issue"

    return None


# -------------------------------
# 🔥 HYBRID CLASSIFIER
# -------------------------------
def classify_log(log):

    # STEP 1: RULES FIRST
    rule_label = rule_based_override(log)
    if rule_label:
        return rule_label

    # STEP 2: ML
    clean_log = preprocess_logs([log])[0]
    embedding = model.encode([clean_log])
    prediction = clf.predict(embedding)[0]

    return prediction


# -------------------------------
# 🚀 MAIN API
# -------------------------------
@app.post("/analyze")
def analyze_logs(request: LogRequest):

    raw_logs = request.logs

    logs = preprocess_logs(raw_logs)
    embeddings = model.encode(logs)

    clustering = DBSCAN(eps=0.5, min_samples=2).fit(embeddings)
    labels = clustering.labels_

    result = {}

    for cluster_id in set(labels):

        cluster_logs = [
            raw_logs[i] for i in range(len(raw_logs)) if labels[i] == cluster_id
        ]

        # 🔴 NOISE → HYBRID
        if cluster_id == -1:
            for log in cluster_logs:
                label = classify_log(log)
                result[label] = result.get(label, 0) + 1

        # 🟢 CLUSTER
        else:
            label = get_root_cause(cluster_logs)
            label_lower = label.lower()

            if "login" in label_lower:
                label = "Successful Login Activity"
            elif "database" in label_lower or "db" in label_lower:
                label = "Database Connectivity Issue"
            elif "payment" in label_lower:
                label = "Payment System Activity"

            # fallback → ML
            if label == "Unknown":
                for log in cluster_logs:
                    fallback = classify_log(log)
                    result[fallback] = result.get(fallback, 0) + 1
                continue

            result[label] = result.get(label, 0) + len(cluster_logs)

    return {
        "total_logs": len(raw_logs),
        "analysis": [
            {
                "issue": label,
                "count": count,
                "solution": get_solution(label),
                "severity": get_severity(label)
            }
            for label, count in result.items()
        ]
    }