#!/usr/bin/python3
import sqlite3

def stream_users():
    # Connect to the database
    conn = sqlite3.connect('your_database.db')  # change 'your_database.db' to your DB path/name
    conn.row_factory = sqlite3.Row  # This lets us fetch rows as dictionaries
    cursor = conn.cursor()

    # Execute query to fetch all users
    cursor.execute("SELECT * FROM user_data")

    # Yield one row at a time
    for row in cursor:
        yield dict(row)

    # Close the connection when done
    cursor.close()
    conn.close()

