import re
import random
import pandas as pd


# -------------------------------
# 🔥 WEB LOG CLEANING (FIRST)
# -------------------------------
def clean_web_log(log):

    # remove IP
    log = re.sub(r'\d+\.\d+\.\d+\.\d+', '', log)

    # remove timestamp
    log = re.sub(r'\[.*?\]', '', log)

    # extract HTTP method + status
    match = re.search(r'"(GET|POST|PUT|DELETE).*?" (\d+)', log, re.IGNORECASE)

    if match:
        method = match.group(1).lower()
        status = match.group(2)

        return f"{method} request status {status}"

    return log


# -------------------------------
# 🔥 GENERAL CLEANING
# -------------------------------
def clean_log(log):

    log = log.lower()

    # remove timestamps (generic)
    log = re.sub(r"\d{4}-\d{2}-\d{2}.*?\s", "", log)

    # remove numbers
    log = re.sub(r"\d+", "", log)

    # remove special characters
    log = re.sub(r"[^\w\s]", "", log)

    return log.strip()


# -------------------------------
# 🔥 NORMALIZATION
# -------------------------------
def normalize_log(log):

    if "database" in log:
        log = log.replace("database", "db")

    if "login successful" in log or "logged in" in log:
        log = "login success"

    if "authentication" in log:
        log = log.replace("authentication", "auth")

    if "failed" in log:
        log = log.replace("failed", "error")

    if "memory" in log:
        log = "memory usage issue"

    return log


# -------------------------------
# 🔥 SINGLE LOG PIPELINE
# -------------------------------
def preprocess_log(log):

    # 👉 STEP 1: detect web log FIRST
    if "HTTP" in log or "GET" in log or "POST" in log:
        log = clean_web_log(log)

    # 👉 STEP 2: normal cleaning
    log = clean_log(log)

    # 👉 STEP 3: normalization
    log = normalize_log(log)

    return log


# -------------------------------
# 🔥 LIST PIPELINE (CORRECT)
# -------------------------------
def preprocess_logs(logs):

    return [preprocess_log(log) for log in logs]


# ===============================
# 🔥 DATASET GENERATION (SAFE)
# ===============================
if __name__ == "__main__":

    logs = [
        "ERROR DB connection timeout",
        "ERROR database connection timed out",
        "DB connection failed error",

        "INFO User login success",
        "User logged in successfully",
        "Login successful for user",

        "WARNING Memory usage high",
        "High memory usage detected",
        "Memory consumption exceeded threshold",

        "ERROR Authentication failed",
        "Invalid credentials login failed",
        "User authentication error",

        "INFO Payment processed",
        "Payment completed successfully",
        "Transaction processed",

        "ERROR Failed to connect to server",
        "Server connection failed",
        "Unable to reach server",

        "CRITICAL Kernel panic system crash",
        "System crash due to kernel panic",

        "FATAL Disk failure data loss",
        "Disk crashed data lost",

        "SECURITY breach detected unauthorized access",
        "Unauthorized access security alert",
    ]

    data = []

    for _ in range(180):
        data.append(random.choice(logs[:6]))

    for _ in range(20):
        data.append(random.choice(logs[6:]))

    clean_logs = preprocess_logs(data)

    df = pd.DataFrame({
        "raw_logs": data,
        "clean_logs": clean_logs
    })

    df.to_csv("data/logs.csv", index=False)

    print("✅ Data saved to data/logs.csv")