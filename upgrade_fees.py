import sqlite3


DATABASE = "data/attendance.db"



conn = sqlite3.connect(
    DATABASE
)


cursor = conn.cursor()



# ==============================
# FEES TABLE
# ==============================

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS fees(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,

    total_amount REAL,

    paid_amount REAL DEFAULT 0,

    pending_amount REAL,

    payment_status TEXT,

    last_payment_date TEXT

)

"""
)



# ==============================
# PAYMENT HISTORY TABLE
# ==============================


cursor.execute(
"""
CREATE TABLE IF NOT EXISTS payments(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,

    amount REAL,

    transaction_id TEXT,

    payment_date TEXT,

    status TEXT

)

"""
)



conn.commit()


conn.close()



print("Fees database created successfully")