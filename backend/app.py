import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from database import init_db, list_tasks
from agent import chat, execute_pending

init_db()

app = Flask(__name__)
CORS(app)

YES = {"yes", "y", "confirm", "confirmed", "proceed", "do it", "okay", "ok"}
NO = {"no", "n", "cancel", "stop", "don't", "do not"}

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/tasks")
def tasks():
    return jsonify(list_tasks())

@app.post("/api/chat")
def chat_endpoint():
    data = request.get_json(force=True)
    message = (data.get("message") or "").strip()
    pending = data.get("pending")

    if not message:
        return jsonify({"reply": "Please enter a message.", "pending": pending})

    if pending and message.lower() in YES:
        result = execute_pending(pending)
        if not result:
            return jsonify({"reply": "I couldn't create the task because the lead was not found.", "pending": None})
        return jsonify({
            "reply": f"Done. I've created task #{result['id']} for {result['lead_name']}.",
            "pending": None
        })

    if pending and message.lower() in NO:
        return jsonify({"reply": "Okay, I won't create the task.", "pending": None})

    try:
        return jsonify(chat(message))
    except Exception as exc:
        return jsonify({"reply": f"Backend error: {exc}", "pending": None}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
