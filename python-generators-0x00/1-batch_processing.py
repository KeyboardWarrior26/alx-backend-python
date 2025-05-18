#!/usr/bin/python3
import sqlite3

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from the user_data table in batches.
    Yields a list of user dicts per batch.
    """
    conn = sqlite3.connect('user_data.db')  # adjust db path if needed
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        columns = [desc[0] for desc in cursor.description]
        batch_dicts = [dict(zip(columns, row)) for row in batch]
        yield batch_dicts

    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """
    Generator that processes batches of users to yield only those with age > 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age', 0) > 25:
                yield user
