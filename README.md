# 📈 IBKR Web API

![Build](https://github.com/danielgmorena/ibkr-web-api/actions/workflows/ci.yml/badge.svg)
![Linted with Ruff](https://img.shields.io/badge/lint-Ruff-%2300bcd4?logo=python&logoColor=white)
![Typed with Mypy](https://img.shields.io/badge/types-Mypy-%232d3f50)
![License](https://img.shields.io/github/license/danielgmorena/ibkr-web-api)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)


An easy-to-use **local web API** for accessing **Interactive Brokers (IBKR)** using [`ib_insync`](https://github.com/erdewit/ib_insync). Designed for end users to run a standalone executable (`ibkr-web-api.exe`) and interact with their local **IB TWS or IB Gateway** instance via HTTP calls.

---

## 🚀 Overview

- ✅ Single-file executable for Windows users: `ibkr-web-api.exe`
- 🧠 Configuration via external `config.yml`
- 🔌 Connects directly to a local TWS or Gateway instance
- 🌐 Exposes a RESTful FastAPI server to query IBKR-TWS data.
- 🔐 Intended for **local use only** (due to TWS dependency)

---

## 📦 Getting Started

### 1. Download the executable

Download the latest release from the [GitHub Releases](https://github.com/danielgmorena/ibkr-web-api/releases) page.

### 2. Prepare a `config.yml` file

Create a `config.yml` file in the same folder or any path of your choice. You can pass its path via command-line argument.

Example:

```yaml
ib:
  host: localhost
  port: 7497

logging:
  level: DEBUG

fastapi:
  title: IBKR Web API
  description: RESTful API for accessing Interactive Brokers historical market data
  version: "1.0"
  docs_url: /docs
  redoc_url: /redoc
  openapi_url: /openapi.json
  debug: false

uvicorn:
  host: "127.0.0.1"
  port: 8000
````

---

## ▶️ Running the App

Ensure your **IB TWS** or **IB Gateway** is running locally on the specified port (default: `7497`).

Then, launch the API server:

```bash
ibkr-web-api.exe --config path\to\your\config.yml
```

If `--config` is omitted, it will use the specified default config.

Once running, access the API via browser or HTTP client:

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## ⚠️ Important Notes

* This app is **intended to run on the same machine as your IBKR TWS/Gateway**.
* It is not designed to be publicly hosted — all communication is assumed to be local (`localhost`).
* All data comes via your authenticated TWS-IBKR session.

---

## 🛠️ Advanced Usage (Developers)

If you're a developer and prefer running from source:

```bash
git clone https://github.com/danielgmorena/ibkr-web-api.git
cd ibkr-web-api
poetry install
poetry run uvicorn app.main:app --reload
```

## 🤝 Contributing

Contributions are welcome!

You can extend this project by wrapping more `ib_insync` functionality as API endpoints. New endpoints should be placed under the `app/api/` directory.

Before submitting a pull request, make sure your code is:

* ✅ **Type-safe** via `mypy`
* ✅ **Linted** via `ruff`
* ✅ **Tested** with `pytest` and includes **coverage**

### Example

To add support for a new IBKR data method:

1. Create a file under `app/api/` (e.g. `app/api/open_orders.py`)
2. Register the router in `app/main.py` or similar
3. Write tests under `tests/`
4. Run:

```bash
mypy app
ruff check .
pytest .
```

Then open a pull request! 🚀

---