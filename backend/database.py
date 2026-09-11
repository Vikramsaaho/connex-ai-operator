import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "connex.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        email TEXT,
        company TEXT,
        phone TEXT,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER NOT NULL,
        task TEXT NOT NULL,
        due_date TEXT,
        status TEXT DEFAULT 'open',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (lead_id) REFERENCES leads(id)
    );
    """)
    leads = [
        ("Sarah Johnson", "sarah@example.com", "Acme Corp", "+44 7000 111111", "Qualified"),
        ("John Smith", "john@example.com", "Tech Ltd", "+44 7000 222222", "New"),
        ("Emily Brown", "emily@example.com", "Nova Systems", "+44 7000 333333", "Contacted"),
    ]
    for lead in leads:
        conn.execute(
            "INSERT OR IGNORE INTO leads(name,email,company,phone,status) VALUES (?,?,?,?,?)",
            lead
        )
    conn.commit()
    conn.close()

def get_lead_info(name):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM leads WHERE lower(name)=lower(?)", (name,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def create_task(lead_name, task, due_date=None):
    conn = get_connection()
    lead = conn.execute(
        "SELECT id FROM leads WHERE lower(name)=lower(?)", (lead_name,)
    ).fetchone()
    if not lead:
        conn.close()
        return None
    cur = conn.execute(
        "INSERT INTO tasks(lead_id,task,due_date) VALUES (?,?,?)",
        (lead["id"], task, due_date)
    )
    conn.commit()
    result = {
        "id": cur.lastrowid, "lead_name": lead_name, "task": task,
        "due_date": due_date, "status": "open"
    }
    conn.close()
    return result

def list_tasks():
    conn = get_connection()
    rows = conn.execute("""
        SELECT tasks.id, leads.name AS lead_name, tasks.task,
               tasks.due_date, tasks.status, tasks.created_at
        FROM tasks JOIN leads ON leads.id = tasks.lead_id
        ORDER BY tasks.id DESC
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]
