# 🧠 AI-Powered Log Analysis System

An AI-based log analysis system that processes unstructured logs and classifies them into issues like security breaches, system failures, and database errors using NLP and Machine Learning.

---

## Features

- Real-time log analysis
- Hybrid classification (Rule-based + ML)
- NLP embeddings using SentenceTransformers
- DBSCAN clustering for pattern detection
- FastAPI backend + Streamlit dashboard
- Trend analysis and visualization

---

## Architecture

Logs → Preprocessing → Embeddings → Clustering → Classification → API → UI

---

## Tech Stack

- Python
- FastAPI
- Streamlit
- Scikit-learn
- SentenceTransformers
- Pandas, NumPy, Matplotlib

---

## How to Run

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/ai-log-analyzer.git

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.api:app --reload

# Run UI
streamlit run app/ui.py