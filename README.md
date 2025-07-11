# 📈 IBKR Web API

A FastAPI-based async web API to access **Interactive Brokers (IBKR)** historical market data via [`ib_insync`](https://github.com/erdewit/ib_insync).

---

## 🔧 Features

- 🚀 Asynchronous FastAPI server
- 🧠 Configuration via `config.yml`
- ⚙️ Connects to IB TWS or IB Gateway
- 📊 Retrieve historical bar data using flexible query parameters
- 🛡️ Ready for production with Uvicorn or Gunicorn + UvicornWorker

---

## 📦 Project Setup (with Poetry)

### 1. Clone the repository

```bash
git clone https://github.com/danielgmorena/ibkr-web-api.git
cd ibkr-web-api
````

### 2. Install dependencies

```bash
poetry install
```

---

## ⚙️ Configuration

### YAML-based config

Edit or create `config.yml` in the project root:

```yaml
ib:
  host: localhost
  port: 7497

fastapi:
  title: IBKR Web API
  description: RESTful API for Interactive Brokers data
  version: 1.0.0
  docs_url: /docs
  redoc_url: /redoc
  openapi_url: /openapi.json
  debug: true

logging:
  level: DEBUG
```

### Environment file (`.env`)

```env
APP_CONFIG=config.yml
```

This enables you to change configs without touching code.

---

## ▶️ Running the App

Make sure your IB TWS or IB Gateway is up and running on the port defined in `config.yml` (`7497` by default).

Start the FastAPI app:

```bash
poetry run uvicorn app.main:app --reload
```

Access the API:

* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🚀 Deploying to Production

Run in production mode:

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```