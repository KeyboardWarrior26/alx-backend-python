import sqlite3
import functools

# Step 3.1: Define the decorator
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else '')
        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

# Step 3.2: Use the decorator on the function
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Step 3.3: Run the function
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
