import os, psycopg2
from flask import Flask

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

@app.route("/")
def home():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY);")
    cur.execute("INSERT INTO visits DEFAULT VALUES;")
    cur.execute("SELECT COUNT(*) FROM visits;")
    count = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return f"Hello from my CI/CD pipeline! Visits: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
