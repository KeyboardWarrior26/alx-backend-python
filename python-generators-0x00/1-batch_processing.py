import sqlite3

def stream_users_in_batches(batch_size):
    """Generator that fetches user rows from the database in batches."""
    conn = sqlite3.connect('users.db')  # Use your actual DB path/name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    
    batch = []
    for row in cursor:
        # Convert row (tuple) to dict with proper keys for clarity
        user = {
            'user_id': row[0],
            'name': row[1],
            'email': row[2],
            'age': row[3]
        }
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
    conn.close()

def batch_processing(batch_size):
    """Generator that processes each batch, yielding users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        # Filter users in batch with age > 25
        filtered_users = (user for user in batch if user['age'] > 25)
        for user in filtered_users:
            yield user
import sqlite3

def stream_users_in_batches(batch_size):
    """Generator that fetches user rows from the database in batches."""
    conn = sqlite3.connect('users.db')  # Use your actual DB path/name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    
    batch = []
    for row in cursor:
        # Convert row (tuple) to dict with proper keys for clarity
        user = {
            'user_id': row[0],
            'name': row[1],
            'email': row[2],
            'age': row[3]
        }
        batch.append(user)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
    conn.close()

def batch_processing(batch_size):
    """Generator that processes each batch, yielding users over age 25."""
    for batch in stream_users_in_batches(batch_size):
        # Filter users in batch with age > 25
        filtered_users = (user for user in batch if user['age'] > 25)
        for user in filtered_users:
            yield user

Checks for use the yield generator

1-batch_processing.py doesn't contain: ["return"]
