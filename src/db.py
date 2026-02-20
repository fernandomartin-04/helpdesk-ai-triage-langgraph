import sqlite3
from pathlib import Path
from typing import Iterable, Dict, Any

BASEDIR = Path(__file__).resolve().parent.parent
DB_PATH = BASEDIR / "data" / "tickets.db"

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db() -> None:
    """
    Creates tables (if they don't exist)
    """
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets_raw (
        ticket_id TEXT PRIMARY KEY,
        
        customer_name TEXT,
        customer_email TEXT,
        customer_age INTEGER,
        customer_gender TEXT,
        product_purchased TEXT,
        date_of_purchase TEXT,
        
        ticket_type TEXT,
        ticket_subject TEXT,
        ticket_description TEXT,
        ticket_status TEXT,
        resolution TEXT,
        ticket_priority TEXT,
        ticket_channel TEXT,
        
        first_response_time TEXT,
        time_to_resolution TEXT,
        customer_satisfaction_rating TEXT,

        has_resolution INTEGER,
        has_time_to_resolution INTEGER,
        has_customer_satisfaction_rating INTEGER,
        has_first_response_time INTEGER);
                     """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets_llm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT NOT NULL,

            llm_ticket_type TEXT,
            llm_ticket_priority TEXT,
            llm_summary TEXT,
            llm_suggested_response TEXT,

            model TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(ticket_id) REFERENCES tickets_raw(ticket_id)
        );
    """)
        conn.execute("""                     
    CREATE UNIQUE INDEX IF NOT EXISTS uq_tickets_llm_all_cols
ON tickets_llm (
  ticket_id,
  COALESCE(llm_ticket_type, ''),
  COALESCE(llm_ticket_priority, ''),
  COALESCE(llm_summary, ''),
  COALESCE(llm_suggested_response, ''),
  COALESCE(model, '')
);
        """)
        conn.commit()

def clean_text(x):
    if x is None:
        return None
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    return s

def upsert_raw_tickets(rows: Iterable[Dict[str, Any]]) -> None:
    sql = """
    INSERT OR IGNORE INTO tickets_raw (
        ticket_id,
        customer_name, customer_email, customer_age, customer_gender,
        product_purchased, date_of_purchase,
        ticket_type, ticket_subject, ticket_description, ticket_status,
        resolution, ticket_priority, ticket_channel,
        first_response_time, time_to_resolution, customer_satisfaction_rating,
        has_resolution, has_time_to_resolution, has_customer_satisfaction_rating, has_first_response_time
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    values = []
    for r in rows:
        ticket_id = clean_text(r.get("Ticket ID"))
        if not ticket_id:
            continue  # o raise ValueError("Missing Ticket ID")

        age_raw = clean_text(r.get("Customer Age"))
        customer_age = int(age_raw) if age_raw and age_raw.isdigit() else None

        values.append((
            ticket_id,

            clean_text(r.get("Customer Name")),
            clean_text(r.get("Customer Email")),
            customer_age,
            clean_text(r.get("Customer Gender")),
            clean_text(r.get("Product Purchased")),
            clean_text(r.get("Date of Purchase")),

            clean_text(r.get("Ticket Type")),
            clean_text(r.get("Ticket Subject")),
            clean_text(r.get("Ticket Description")),
            clean_text(r.get("Ticket Status")),
            clean_text(r.get("Resolution")),
            clean_text(r.get("Ticket Priority")),
            clean_text(r.get("Ticket Channel")),

            clean_text(r.get("First Response Time")),
            clean_text(r.get("Time to Resolution")),
            clean_text(r.get("Customer Satisfaction Rating")),

            int(bool(r.get("has_Resolution", 0))),
            int(bool(r.get("has_Time to Resolution", 0))),
            int(bool(r.get("has_Customer Satisfaction Rating", 0))),
            int(bool(r.get("has_First Response Time", 0))),
        ))

    with get_connection() as conn:
        conn.executemany(sql, values)
        conn.commit()


def insert_llm_result(state: Dict[str, Any]) -> None:
    """
    Inserta una ejecución del LLM (histórico) para un ticket_id existente.
    """
    sql = """
    INSERT OR IGNORE INTO tickets_llm (
        ticket_id,
        llm_ticket_type, llm_ticket_priority, llm_summary, llm_suggested_response,
        model
    )
    VALUES (?, ?, ?, ?, ?, ?);
    """

    with get_connection() as conn:
        conn.execute(sql, (
            str(state.get("ticket_id")),
            state.get("ticket_type"),
            state.get("ticket_priority"),
            state.get("summary"),
            state.get("suggested_response"),
            state.get("model"),
        ))
        conn.commit()


