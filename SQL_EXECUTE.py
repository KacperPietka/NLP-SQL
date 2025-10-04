import sqlite3

conn = sqlite3.connect("example.db")
cursor = conn.cursor()
cursor.execute(sql_query)
rows = cursor.fetchall()