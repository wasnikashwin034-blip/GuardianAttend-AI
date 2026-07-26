import sqlite3


conn = sqlite3.connect(
    "data/attendance.db"
)

cursor = conn.cursor()


# Add status column

try:

    cursor.execute(
        """
        ALTER TABLE attendance
        ADD COLUMN status TEXT
        """
    )

    print("status column added")

except Exception:

    print("status already exists")



# Add confidence column

try:

    cursor.execute(
        """
        ALTER TABLE attendance
        ADD COLUMN confidence REAL
        """
    )

    print("confidence column added")

except Exception:

    print("confidence already exists")



conn.commit()

conn.close()


print("Database upgrade completed")