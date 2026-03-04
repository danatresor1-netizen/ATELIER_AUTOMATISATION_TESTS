import sqlite3
import json
from datetime import datetime

def init_db():
    conn = sqlite3.connect("runs.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            passed INTEGER,
            failed INTEGER,
            latency_avg REAL,
            latency_p95 REAL,
            json_run TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_run(run):
    conn = sqlite3.connect("runs.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO runs (timestamp, passed, failed, latency_avg, latency_p95, json_run)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        run["passed"],
        run["failed"],
        run["latency_avg"],
        run["latency_p95"],
        json.dumps(run)
    ))
    conn.commit()
    conn.close()

def list_runs():
    conn = sqlite3.connect("runs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM runs ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows
