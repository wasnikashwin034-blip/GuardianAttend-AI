import sqlite3
import os

DATABASE = "data/attendance.db"


def init_database():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        total_amount REAL,
        paid_amount REAL,
        pending_amount REAL,
        payment_status TEXT,
        last_payment_date TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        amount REAL,
        transaction_id TEXT,
        payment_date TEXT,
        status TEXT
    )
    """)


    conn.commit()
    conn.close()