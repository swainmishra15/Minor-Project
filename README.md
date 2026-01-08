# 🚀 AI-Driven Site Monitoring, Log Intelligence & Crash Prediction System

An **AI-powered system monitoring and crash prediction platform** that combines **Machine Learning, NLP, Backend APIs, and DevOps monitoring** to detect issues early and predict system failures.

This project was developed by a **team of three** under the **guidance of a faculty mentor** as part of an academic project.

---

## 📌 Features

- 📊 Real-time **system metrics collection** (CPU, memory, disk, network)
- 🧠 **Log classification** using a **fine-tuned BART NLP model**
- 🔍 Automatic categorization of logs (error, warning, info, security, performance, etc.)
- 📈 **Crash risk prediction** using machine learning models
- ⏱️ **Time-to-crash estimation**
- 📡 **Prometheus integration** for monitoring and observability
- 🗄️ Centralized log and prediction storage using **PostgreSQL**
- 🌐 REST APIs built with **FastAPI**
- ⚙️ Designed following **DevOps monitoring practices**

---

## 🧠 Machine Learning & NLP

- Used **facebook/bart-large-mnli** as the base NLP model
- Fine-tuned the model specifically for **log classification**
- Additional ML models used for:
  - Crash prediction
  - Time-to-crash regression
- Models are loaded using `.pkl` and HuggingFace model files

---

## 🛠️ Tech Stack

### 🔹 Backend

- FastAPI
- Uvicorn
- Pydantic

### 🔹 Machine Learning

- PyTorch
- HuggingFace Transformers (BART)
- NumPy
- Pandas
- Joblib

### 🔹 Monitoring & DevOps

- Prometheus
- prometheus_client
- prometheus_fastapi_instrumentator
- psutil

### 🔹 Database

- PostgreSQL
- psycopg2

---

## 📂 Project Structure

```
Minor-Project/
│
├── backend/
│   ├── classifier.py
│   ├── collector.py
│   ├── database.py
│   ├── metrics.py
│   ├── prom_query.py
│   └── main.py
│
├── models/
│   ├── final_log_classifier/
│   ├── final_crash_model.pkl
│   ├── final_scaler.pkl
│   ├── time_to_crash_regressor.pkl
│   └── time_to_crash_scaler.pkl
│
├── log_sender.py
├── live_log_sender.ps1
└── README.md
```

---

## ⚙️ How It Works

1. System metrics are collected using `psutil`
2. Logs are sent to the backend via API
3. Logs are classified using the fine-tuned BART model
4. Error and warning trends are analyzed
5. ML models predict:
   - Crash risk
   - Estimated time to crash
6. Metrics are exposed to Prometheus
7. Data is stored in PostgreSQL for analysis

---

## ▶️ Running the Project (Localhost)

### 1️⃣ Start PostgreSQL & Prometheus

Make sure PostgreSQL and Prometheus are running locally.

### 2️⃣ Start Backend Server

```bash
uvicorn main:app --reload
```

### 3️⃣ Access API Docs

Open your browser and navigate to:

```
http://localhost:8000/docs
```

### 4️⃣ Send Logs

Run the log sender script:

```bash
python log_sender.py
```

---

## 📊 Monitoring

**Prometheus** scrapes metrics from the backend. The `/metrics` endpoint exposes system and application metrics that can be visualized using **Grafana** (optional).

---

## 📝 License

This project is part of an academic initiative and is available for educational purposes.

---

## 👥 Team

Developed by a dedicated team of three students under faculty mentorship.
