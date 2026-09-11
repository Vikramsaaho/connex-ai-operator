# ConneX AI Operator

A lightweight AI-operator-style CRM application built with **React, Flask, and SQLite**. The application allows users to look up CRM leads and create follow-up tasks through a simple conversational interface.

The current implementation uses **local rule-based task and lead handling**, so it does not require an OpenAI API key or external AI service.

## Features

* 💬 Conversational CRM interface
* 🔎 Lead information lookup
* 📋 Create follow-up tasks
* ✅ Confirmation before creating tasks
* 📅 Support for task due dates such as "tomorrow"
* 💾 SQLite database persistence
* 🌐 React frontend
* ⚙️ Flask REST API backend
* 🔐 No API key required for the current implementation

## Tech Stack

### Frontend

* React
* Vite
* JavaScript
* CSS

### Backend

* Python
* Flask
* Flask-CORS
* SQLite

## Project Structure

```text
connex-ai-operator/
│
├── backend/
│   ├── agent.py
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## How It Works

The application has two main components:

```text
┌──────────────────────┐
│   React Frontend     │
│   Chat Interface     │
└──────────┬───────────┘
           │ HTTP API
           ▼
┌──────────────────────┐
│    Flask Backend     │
│  CRM Operator Logic  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    SQLite Database   │
│ Leads + Tasks        │
└──────────────────────┘
```

The frontend sends user messages to the Flask backend. The backend interprets the request, looks up leads, asks for confirmation before write actions, and stores confirmed tasks in SQLite.

## Backend Setup

Open a terminal and run:

```bash
cd backend
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Start the backend:

```powershell
python app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

## Frontend Setup

Open a second terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

Open the URL in your browser.

## Example Usage

### Look up a lead

```text
Tell me about Sarah Johnson
```

Example response:

```text
Here is the lead information:

Id: 1
Name: Sarah Johnson
Email: sarah@example.com
Company: Acme Corp
Phone: +44 7000 111111
Status: Qualified
```

### Create a follow-up task

```text
Create a task to call Sarah Johnson tomorrow
```

The operator asks for confirmation:

```text
I can create a follow-up task for Sarah Johnson:
"call" for tomorrow.
Would you like me to proceed?
```

Confirm:

```text
yes
```

The task is then stored in SQLite.

## API Endpoints

### Health Check

```http
GET /api/health
```

Returns:

```json
{
  "status": "ok"
}
```

### Get Tasks

```http
GET /api/tasks
```

Returns the stored tasks.

### Chat

```http
POST /api/chat
```

Example request:

```json
{
  "message": "Tell me about Sarah Johnson"
}
```

## Safety and Confirmation

The operator requires explicit confirmation before performing write actions.

For example:

```text
User:
Create a task to call Sarah Johnson tomorrow

Operator:
I can create a follow-up task for Sarah Johnson.
Would you like me to proceed?

User:
yes

Operator:
Done. I've created task #1 for Sarah Johnson.
```

This prevents accidental task creation from conversational requests.

## Current Limitations

* The current operator uses local rule-based intent detection.
* Lead matching depends on the data available in the SQLite database.
* The application is currently designed as a local development prototype.
* Authentication and production deployment are not currently implemented.

## Future Improvements

* Integrate a local or hosted LLM
* Add authentication and user accounts
* Add more CRM actions
* Add task editing and deletion
* Add natural-language date parsing
* Add lead creation and updating
* Add production database support
* Add automated tests
* Deploy the frontend and backend

## Demo

Try these commands:

```text
Tell me about Sarah Johnson
```

```text
Create a task to call Sarah Johnson tomorrow
```

```text
yes
```

## License

This project is intended as a prototype and portfolio project.

