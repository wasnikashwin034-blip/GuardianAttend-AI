import sqlite3


conn = sqlite3.connect(
    "data/attendance.db"
)

cursor = conn.cursor()


try:

    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN name TEXT
        """
    )

    print("name column added")

except:

    pass



try:

    cursor.execute(
        """
        ALTER TABLE users
        ADD COLUMN email TEXT
        """
    )

    print("email column added")

except:

    pass



conn.commit()

conn.close()


print("User table upgraded")