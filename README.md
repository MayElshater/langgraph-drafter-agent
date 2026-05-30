# 🚀 AI Document Drafting Agent

A production-ready AI Agent built with LangGraph, Gemini 2.5 Flash, FastAPI, React, and Docker.

This project demonstrates agentic workflows, tool calling, document generation, document editing, and file saving capabilities through a modern web interface.

---

## 📸 Demo



### Application Interface

<img width="1347" height="764" alt="Screenshot 2026-05-26 005521" src="https://github.com/user-attachments/assets/5fd627b9-ba00-4bf2-bde7-796e975dc53d" />


### Agent Reasoning & Tool Calling

<img width="1350" height="764" alt="Screenshot 2026-05-30 193354" src="https://github.com/user-attachments/assets/41134138-29ed-4256-adec-e29f488f899f" />


### Docker Deployment

<img width="1250" height="711" alt="Screenshot 2026-05-30 183218" src="https://github.com/user-attachments/assets/0b23d1e8-5da0-41c3-9849-9cb1294ff111" />


---

## 🎥 Demo Video

Watch the project demo:

https://youtu.be/Z2ewBEjfoXM

---

## ✨ Features

* AI-powered document drafting
* LangGraph agent orchestration
* Tool Calling architecture
* Update Document Tool
* Save Document Tool
* Session-based document management
* Real-time document preview
* FastAPI REST API backend
* React frontend interface
* Dockerized deployment
* Google Vertex AI integration

---

## 🏗️ System Architecture

```text
React Frontend
       │
       ▼
FastAPI Backend
       │
       ▼
LangGraph Agent
       │
       ├── Update Document Tool
       ├── Save Document Tool
       │
       ▼
Gemini 2.5 Flash (Vertex AI)
```

The agent reasons about user requests, selects the appropriate tool, updates the document state, and returns responses through the API layer.

---

## 🛠️ Tech Stack

### AI & Backend

* Python 3.11
* LangGraph
* LangChain
* Gemini 2.5 Flash
* Google Vertex AI
* FastAPI

### Frontend

* React
* Vite

### DevOps

* Docker
* Docker Compose

---

## 📂 Project Structure

```text
langgraph-drafter-app/
│
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## ⚙️ Environment Variables

Create:

```bash
backend/.env
```

Example:

```env
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GEMINI_MODEL=gemini-2.5-flash
```

Never commit secrets or credentials to GitHub.

---

## 🔐 Google Cloud Authentication

Authenticate locally:

```bash
gcloud auth application-default login
gcloud config set project your-project-id
```

Ensure Vertex AI API is enabled and billing is configured.

---

## 🚀 Run Locally

### Backend

```bash
cd backend

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Open:

```text
http://localhost:5173
```

API Docs:

```text
http://localhost:8000/docs
```

---

## 🐳 Run with Docker

Create:

```bash
backend/.env
```

Then:

```bash
docker compose up --build
```

Services:

```text
Frontend → http://localhost:5173
Backend  → http://localhost:8000
```

---

## 📦 Docker Images

Backend:

```bash
docker pull mayrashad98/langgraph-drafter-backend:latest
```

Frontend:

```bash
docker pull mayrashad98/langgraph-drafter-frontend:latest
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Chat

```http
POST /chat
```

Request:

```json
{
  "session_id": "demo-session",
  "message": "Create a proposal for WhatsApp automation using n8n"
}
```

### Save Document

```http
POST /save
```

### Get Current Document

```http
GET /document/{session_id}
```

---

## 🎯 Portfolio Highlights

This project demonstrates:

* AI Agent Design
* Tool Calling Workflows
* LangGraph Orchestration
* Gemini Integration
* FastAPI Development
* React Frontend Development
* Docker Containerization
* Full-Stack AI Engineering

---

## 🔮 Future Improvements

* Persistent Database Storage
* User Authentication
* Streaming Responses
* File Downloads
* Multi-user Sessions
* Cloud Deployment
* RAG Integration

---

## 👩‍💻 Author

May Elshater

AI Engineer | Automation Engineer

Specialized in:

* AI Agents
* Workflow Automation
* LangGraph
* LLM Applications
* FastAPI
* Docker
