# LangGraph Drafter App

A portfolio-ready fullstack AI document drafting app built with LangGraph, FastAPI, React, and Google Cloud Vertex AI. The app turns a terminal-based drafting agent into a browser demo where users can chat with an AI writing assistant, preview the evolving document, see tool activity, and save the final draft as a `.txt` file.

## Architecture

```text
React Vite UI  ->  FastAPI API  ->  LangGraph Agent  ->  Gemini on Vertex AI
                      |
                      +-> In-memory session document state
                      +-> Local .txt document saving
```

The backend keeps demo session state in memory. Each `session_id` has its own chat messages and document content, which keeps the app simple for portfolio demos without adding a database.

## Tech Stack

- Python 3.11
- FastAPI
- LangGraph
- LangChain Google Vertex AI
- Gemini 2.5 Flash
- React + Vite
- Docker Compose

## Project Structure

```text
langgraph-drafter-app/
├── backend/
│   ├── main.py
│   ├── agent.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

## Environment Variables

Create `backend/.env` from the example file:

```bash
cp backend/.env.example backend/.env
```

Then set:

```env
GCP_PROJECT_ID=your-google-cloud-project-id
GCP_LOCATION=us-central1
GEMINI_MODEL=gemini-2.5-flash
```

No secrets should be committed to GitHub. Keep real credentials and `.env` files local.

## Google Cloud Authentication

This app uses Vertex AI, so your local environment or container needs Google Cloud credentials with access to Vertex AI.

For local development, authenticate with:

```bash
gcloud auth application-default login
gcloud config set project your-google-cloud-project-id
```

Make sure the Vertex AI API is enabled for the project.

For Docker, provide credentials using your preferred secure workflow, such as mounting an application-default credentials file or using a service account in your deployment environment. Do not copy credential JSON files into the repository.

## Run Locally

Start the backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Start the frontend in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

FastAPI docs are available at:

```text
http://localhost:8000/docs
```

## Run With Docker

Create `backend/.env`, then run:

```bash
docker compose up --build
```

Services:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

## API Endpoints

### `GET /health`

Returns:

```json
{ "status": "ok" }
```

### `POST /chat`

Request:

```json
{
  "session_id": "demo-session",
  "message": "Write a short cover letter for a junior AI engineer role."
}
```

Response:

```json
{
  "ai_message": "Done. I drafted a concise cover letter...",
  "document_content": "Dear Hiring Manager...",
  "tool_used": "update_document",
  "tool_result": "Document updated successfully."
}
```

### `GET /document/{session_id}`

Returns the current document content for a session.

### `POST /save`

Request:

```json
{
  "session_id": "demo-session",
  "filename": "cover-letter.txt"
}
```

Saves the document into `backend/saved_documents/`.

## Demo Flow

1. Open the frontend.
2. Ask the agent to draft a document, such as a cover letter, email, or project proposal.
3. Ask for revisions: shorter, more professional, more persuasive, or formatted with bullets.
4. Watch the document preview update after tool calls.
5. Save the document with the save button.

## Portfolio Notes

This project intentionally uses in-memory state to keep the demo easy to understand and fast to run. A production version could add persistent storage, authentication, file downloads, streaming responses, and deployment-specific Google Cloud identity.
