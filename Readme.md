# 🧠 AI-Powered Log Analysis System

An end-to-end AI system that automatically analyzes unstructured system logs and detects critical issues such as security breaches, system failures, authentication errors, and database problems using NLP and Machine Learning.

---

## Overview

Modern applications generate massive volumes of logs, making manual monitoring inefficient and error-prone.
This project solves that by building a **hybrid AI pipeline (Rule-based + ML)** to automatically classify logs and provide actionable insights in real time.

---

## Key Features

* 🔍 Automated log classification (Security, System, Auth, DB, Web)
* 🧠 Hybrid AI system (Rule-based + Machine Learning)
* 📊 Interactive dashboard (Bar chart, Pie chart, Trend analysis)
* 📈 Real-time issue monitoring
* 🌐 Supports real-world logs (Apache, system logs, authentication logs)

---

## Architecture

Logs → Preprocessing → Embeddings → Clustering → Classification → FastAPI → Streamlit Dashboard

---

## Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **ML Model:** Logistic Regression
* **NLP:** SentenceTransformers (all-MiniLM-L6-v2)
* **Clustering:** DBSCAN
* **Libraries:** Pandas, NumPy, Matplotlib

---

## Model Performance

* Accuracy: **~94%**
* Evaluated using:

  * Precision
  * Recall
  * F1-score
* Handles multiple categories:

  * Security Breach
  * System Crash
  * Authentication Failure
  * Database Issues
  * Web Requests

---

## How to Run

### 1. Clone Repository

```bash
git clone https://github.com/Sunilyadav816/ai-log-analyzer.git
cd ai-log-analyzer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend

```bash
uvicorn app.api:app --reload
```

### 4. Run Frontend

```bash
streamlit run app/ui.py
```

---

## 📈 Example Output

```
🔴 High | Server Error → 2 logs  
🟡 Medium | Database Connectivity Issue → 1 logs  
🟢 Low | Successful Login Activity → 2 logs  
```

---



## 🔮 Future Improvements

* Anomaly Detection (Isolation Forest)
* Cloud Deployment (AWS / Render)
* Real-time log streaming (Kafka)
* Confidence scoring for predictions

---

## 👨‍💻 Author

* GitHub: https://github.com/Sunilyadav816
* LinkedIn: https://www.linkedin.com/in/sunil-yadav1010/

---

⭐ If you found this useful, give it a star!
