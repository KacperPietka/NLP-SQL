import json
import snowflake.connector
from PyQt6.QtCore import QSettings
import decimal

def json_safe(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def execute_sql_query(sql_query):
    """
    Executes a SQL query on the user's connected Snowflake account
    and returns results as a JSON string.
    """

    # --- Load saved connection info from QSettings ---
    settings = QSettings("SQLNLPApp", "Snowflake")

    user = settings.value("user")
    password = settings.value("password")
    account = settings.value("account")
    warehouse = settings.value("warehouse")
    database = settings.value("database")
    schema = settings.value("schema")

    if not all([user, password, account, warehouse, database, schema]):
        raise Exception("❌ Missing Snowflake credentials. Please connect first.")

    # --- Connect to Snowflake ---
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema
    )

    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        # Convert results to list of dicts
        results = [dict(zip(columns, row)) for row in rows]

        # Return as pretty JSON string
        return json.dumps(results, indent=2, default=json_safe)

    except snowflake.connector.errors.ProgrammingError as e:
        raise Exception(f"❌ Snowflake SQL error: {e}")

    finally:
        cursor.close()
        conn.close()
