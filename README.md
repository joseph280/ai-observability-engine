# 🔍 AI Observability Engine

[![CI Pipeline](https://github.com/joseph280/ai-observability-engine/actions/workflows/test.yml/badge.svg)](https://github.com/joseph280/ai-observability-engine/actions)
![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

A high-performance, asynchronous middleware for monitoring, evaluating, and analyzing Large Language Model (LLM) interactions. Designed with a **Service-Repository pattern**, fully containerized, and backed by comprehensive CI/CD.

---

## 🚀 Features

* **⚡ Async Engine:** Non-blocking task execution using Python's `asyncio` and `uvloop`.
* **🧠 LLM Evaluation:** Automated quality scoring of AI responses (Hallucination detection, tone checks).
* **📊 Real-time Analytics:** Tracks pass rates, latency, and token usage via a dedicated Metrics Service.
* **🐳 Dockerized:** One-command deployment for immediate reproducibility.
* **🛡️ Robust Testing:** Integration tests and CI/CD pipeline via GitHub Actions.

---

## 🏗️ Architecture

The application follows a **Modular Monolith** architecture:

1.  **API Layer (FastAPI):** Handles HTTP requests and schema validation (Pydantic V2).
2.  **Service Layer:** Contains business logic (Analytics, Task Runner) decoupled from the DB.
3.  **Core Engine:** Manages LLM interactions and evaluation prompts.
4.  **Data Layer (SQLAlchemy):** Persists tasks and metrics to SQLite (easily swappable for PostgreSQL).

---

## 🛠️ Quick Start

### Option 1: Using Docker (Recommended)
Ensure you have Docker Desktop installed.

```bash
# 1. Clone the repository
git clone https://github.com/josephaguilarfeener/ai-observability-engine.git
cd ai-observability-engine

# 2. Set up environment variables
cp .env.example .env
# (Open .env and add your OPENAI_API_KEY)

# 3. Run the container
docker compose up --build
```

### Option 2: Local Development

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run server
uvicorn app.main:app --reload
```

---

## 🧪 Testing

This project uses Pytest for unit and integration testing. The CI pipeline runs these tests on every push.

```bash
# Run all tests
docker compose run api pytest

# OR locally
pytest tests/
```

---

## 📚 API Documentation

Once running, explore the interactive Swagger UI:

* **Docs:** `http://localhost:8000/docs`
* **Redoc:** `http://localhost:8000/redoc`

---

## 🔮 Roadmap

- [ ] Add Redis for caching frequent metric queries.
- [ ] Integrate Prometheus/Grafana for dashboard visualization.
- [ ] Add user authentication (OAuth2).

---

Built by **Joseph Aguilar Feener** as part of a 14-Day AI Engineering Sprint.
