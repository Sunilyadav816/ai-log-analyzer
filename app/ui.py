import streamlit as st
import requests
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AI Log Analyzer", layout="wide")

st.title("🧠 AI Log Analyzer")

API_URL = "http://127.0.0.1:8000/analyze"

# -------------------------------
# 🔥 STATE INIT
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# INPUT SECTION
# -------------------------------
st.subheader("📋 Input Logs")

col1, col2 = st.columns(2)

with col1:
    log_input = st.text_area("Paste logs (one per line)", height=200)

with col2:
    uploaded_file = st.file_uploader("Upload .txt file", type=["txt"])

logs = []

if log_input:
    logs.extend([log.strip() for log in log_input.split("\n") if log.strip()])

if uploaded_file:
    content = uploaded_file.read().decode("utf-8")
    file_logs = [log.strip() for log in content.split("\n") if log.strip()]
    logs.extend(file_logs)

# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("🚀 Analyze Logs"):

    if not logs:
        st.warning("⚠️ Please provide logs")

    else:
        with st.spinner("Analyzing logs..."):

            response = requests.post(API_URL, json={"logs": logs})
            data = response.json()
            analysis = data["analysis"]

            # -------------------------------
            # 🔥 STORE TREND DATA
            # -------------------------------
            timestamp = time.strftime("%H:%M:%S")
            trend_entry = {"time": timestamp}

            for item in analysis:
                trend_entry[item["issue"]] = item["count"]

            st.session_state.history.append(trend_entry)

            # -------------------------------
            # 📊 ANALYSIS RESULT
            # -------------------------------
            st.subheader("📊 Analysis Result")

            # 🔴 High severity alert
            high_issues = [i for i in analysis if i["severity"] == "High"]
            total_high = sum(i["count"] for i in high_issues)

            if total_high > 0:
                st.error(f"🚨 {total_high} High Severity Log(s) Detected!")

            # -------------------------------
            # 📊 DASHBOARD (SIDE BY SIDE)
            # -------------------------------
            col1, col2 = st.columns(2)

            issues = [item["issue"] for item in analysis]
            counts = [item["count"] for item in analysis]

            # BAR CHART
            with col1:
                fig1 = plt.figure(figsize=(5, 4))
                plt.bar(issues, counts)
                plt.xticks(rotation=30, ha='right')
                plt.title("Issue Distribution")
                plt.xlabel("Issue")
                plt.ylabel("Count")
                plt.tight_layout()
                st.pyplot(fig1)

            # PIE CHART
            with col2:
                severity_count = {}
                for item in analysis:
                    sev = item["severity"]
                    severity_count[sev] = severity_count.get(sev, 0) + item["count"]

                fig2 = plt.figure(figsize=(5, 4))
                plt.pie(
                    severity_count.values(),
                    labels=severity_count.keys(),
                    autopct='%1.1f%%'
                )
                plt.title("Severity Distribution")
                plt.tight_layout()
                st.pyplot(fig2)

            # -------------------------------
            # 📋 DETAILED ANALYSIS
            # -------------------------------
            st.subheader("📋 Detailed Analysis")

            for item in analysis:
                count = item["count"]
                severity = item["severity"]

                emoji = "🔴" if severity == "High" else "🟡" if severity == "Medium" else "🟢"

                st.write(f"{emoji} {severity} | {item['issue']} → {count} logs")
                st.write(f"💡 {item['solution']}")
                st.write("---")

# -------------------------------
# 📈 TREND ANALYSIS
# -------------------------------
st.subheader("📈 Trend Analysis")

history = st.session_state.history

if len(history) > 1:

    all_issues = set()
    for entry in history:
        all_issues.update(entry.keys())

    all_issues.discard("time")

    fig = plt.figure(figsize=(8, 4))

    for issue in all_issues:
        values = []
        times = []

        for entry in history:
            times.append(entry["time"])
            values.append(entry.get(issue, 0))

        plt.plot(times, values, marker='o', label=issue)

    plt.xticks(rotation=30)
    plt.xlabel("Time")
    plt.ylabel("Log Count")
    plt.title("Issue Trends Over Time")
    plt.legend()
    plt.tight_layout()

    st.pyplot(fig)

else:
    st.info("Analyze logs multiple times to see trend analysis")