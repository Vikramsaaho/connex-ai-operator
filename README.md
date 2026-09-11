# ConneX AI Operator

React + Flask + OpenAI + SQLite AI Operator challenge project.

## Features
- Ask tool: `get_lead_info`
- Run tool: `create_follow_up_task`
- Confirmation before write actions
- SQLite persistence
- Simple chat interface

## Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` with your OpenAI API key and model, then:
```bash
python app.py
```

## Frontend
In another terminal:
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## Demo
1. `Tell me about Sarah Johnson`
2. `Create a task to call Sarah Johnson tomorrow`
3. Confirm with `Yes`
