import sqlite3
import json

def execute_sql_query(sql_query):
    """
    Executes a SQL query on example.db and returns the results as a JSON string.
    """
    conn = sqlite3.connect("databases/example.db")
    conn.row_factory = sqlite3.Row  # Makes rows behave like dicts
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Convert to list of dictionaries
        results = [dict(row) for row in rows]

        # Return pretty-formatted JSON
        return json.dumps(results, indent=2)

    except sqlite3.Error as e:
        raise Exception(f"SQL execution error: {e}")

    finally:
        conn.close()
