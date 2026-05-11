import os
import psycopg2
from flask import Flask
from datetime import datetime

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_NAME = os.getenv("DB_NAME", "hello_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "password")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

@app.route("/")
def hello():
    name = os.getenv("NAME", "Guest")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS simple_hits (id SERIAL PRIMARY KEY);")
    cur.execute("INSERT INTO simple_hits DEFAULT VALUES;")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM simple_hits;")
    total_hits = cur.fetchone()[0]

    cur.close()
    conn.close()

    return f"<h1>Hello {name}!</h1><p>This page has been viewed {total_hits} times.</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)