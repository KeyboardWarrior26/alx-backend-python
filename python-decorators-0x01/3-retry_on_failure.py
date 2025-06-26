import time
import sqlite3
import functools

# Reuse: with_db_connection from previous tasks
def with_db_connection(func):
    """Decorator to open and close DB connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# New: retry_on_failure decorator
def retry_on_failure(retries=3, delay=2):
    """Retry decorator for transient database failures."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == retries:
                        print("All retries failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# Function that uses both decorators
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Run and test
users = fetch_users_with_retry()
print(users)
