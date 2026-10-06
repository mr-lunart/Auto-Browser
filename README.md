# Knowledge Engine

**An agent-ready browser automation desktop app** — a PySide6 + Streamlit front-end built to host an AI agent that sees, reasons, and drives a real Chromium browser over the Chrome DevTools Protocol (CDP).

Knowledge Engine wraps a Streamlit web app inside a native Qt desktop window, giving you a polished, installable UI for an agentic system that is planned to be powered by **LangGraph** and **MCP Playwright**.

## ✨ Highlights

- 🖥️ **Desktop-native UX** — PySide6 (`QMainWindow` + `QWebEngineView`) hosting a Streamlit app, with graceful server lifecycle (auto-start, readiness polling, clean shutdown)
- 💬 **Built-in chat interface** — Streamlit chat UI with typed message rendering (text / success / warning / info / error) and persistent session history
- 📊 **Status dashboard** — live OS info, browser process state, and chat statistics
- 🌐 **CDP-ready browser launcher** — one-click launch of Chromium with `--remote-debugging-port=9222`, PID-tracked with stale-process detection
- 🤖 **Agent-first backend** — FastAPI service exposing LangGraph flows (`/run_chatbot`, `/run_query`) with thread-scoped state
- 🔌 **MCP Playwright roadmap** — designed so the LangGraph agent controls Chromium through MCP Playwright over CDP

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  PySide6 Desktop Shell (app.py)             │
│  ┌───────────────────────────────────────┐  │
│  │  QWebEngineView ──▶ Streamlit :8501   │  │
│  │   • Chat page (ui.py)                 │  │
│  │   • Status page (status_page.py)      │  │
│  └───────────────────────────────────────┘  │
└──────────────────┬──────────────────────────┘
                   │ HTTP
        ┌──────────▼───────────┐
        │  FastAPI (main.py)   │
        │  /run_chatbot        │
        │  /run_query          │
        └──────────┬───────────┘
                   │
        ┌──────────▼────────────────────┐
        │  LangGraph flows (planned)    │
        │  GraphFlow · RetrivalGraph    │
        └──────────┬────────────────────┘
                   │ MCP
        ┌──────────▼────────────────────┐
        │  MCP Playwright ──CDP:9222──▶ │
        │  Chromium browser             │
        └───────────────────────────────┘
```

## 🧰 Tech Stack

| Layer | Technology |
| --- | --- |
| Desktop shell | PySide6 6.10 (Qt WebEngine) |
| Web UI | Streamlit |
| Agent framework | LangGraph 1.2 |
| LLM tooling | pydantic-ai (OpenAI) |
| Backend API | FastAPI |
| Browser control | Playwright via MCP over CDP |
| Config | python-dotenv |

## 📁 Project Structure

```
.
├── app.py            # PySide6 shell: launches Streamlit, embeds it in Qt browser
├── entry.py          # Streamlit entry point (page navigation)
├── ui.py             # Chat page + browser launcher (CDP :9222)
├── status_page.py    # Status dashboard
├── main.py           # FastAPI service with LangGraph flows
├── graphflow.py      # (placeholder) graph flow module
├── requirements.txt  # Python dependencies
└── .env              # Environment variables (not tracked)
```

> The agent backend package (`src/graphflow`) is a work-in-progress and intentionally excluded from this repository via `.gitignore`.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Chromium (Linux) or Google Chrome (macOS) installed and on `PATH`

### Install

```bash
git clone <repo-url>
cd "Auto Browser"
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
# Launch the desktop app (starts Streamlit automatically on :8501)
python app.py

# Or run the Streamlit UI directly
streamlit run entry.py --server.port 8501
```

In the **Chat** page, click **"Check OS and Launch Browser"** in the sidebar to start Chromium with remote debugging enabled on port `9222`.

### API

The FastAPI service (once the agent graphs are wired in) exposes:

| Endpoint | Body | Description |
| --- | --- | --- |
| `POST /run_chatbot` | `{"query": "...", "thread_id": "..."}` | Run the chatbot graph flow |
| `POST /run_query` | `{"query": "...", "thread_id": "..."}` | Run the retrieval graph flow |

## 🗺️ Roadmap

- [ ] Implement `src/graphflow` — LangGraph `GraphFlow` and `RetrivalGraph` compilation
- [ ] Connect the LangGraph agent to **Playwright MCP server**
- [ ] Drive Chromium via **CDP** (`ws://localhost:9222`) for browser automation tasks
- [ ] Surface agent actions / observations in the chat UI
- [ ] Windows support for browser launch

## 📄 License

POC / private project.
