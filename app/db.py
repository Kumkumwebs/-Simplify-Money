from pathlib import Path
import sqlite3
from datetime import datetime

DB_PATH = Path(__file__).resolve().parents[1] / "gold_purchases.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            name TEXT,
            phone TEXT,
            amount_inr REAL,
            grams REAL,
            price_per_gram_inr REAL,
            timestamp_utc TEXT,
            status TEXT
        )
        """
    )
    con.commit()
    con.close()

def insert_purchase(
    user_id: str,
    name: str,
    phone: str,
    amount_inr: float,
    grams: float,
    price_per_gram_inr: float,
    status: str = "SUCCESS",
):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    ts = datetime.utcnow().isoformat()
    cur.execute(
        """
        INSERT INTO purchases
        (user_id, name, phone, amount_inr, grams, price_per_gram_inr, timestamp_utc, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, name, phone, amount_inr, grams, price_per_gram_inr, ts, status),
    )
    con.commit()
    txn_id = cur.lastrowid
    con.close()
    return txn_id, ts
