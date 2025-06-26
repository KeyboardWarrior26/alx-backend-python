import time
import sqlite3
import functools

query_cache = {}

# Reuse from previous tasks
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

# New: cache_query decorator
def cache_query(func):
    """Cache query results based on SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Returning cached result for:", query)
            return query_cache[query]
        print("Executing and caching result for:", query)
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First call result:", users)

# Second call will use the cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second call result:", users_again)
