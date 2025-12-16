from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'mysql'),
        user=os.getenv('DB_USER', 'ubuntu'),
        password=os.getenv('DB_PASSWORD', '1234'),
        database=os.getenv('DB_NAME', 'kubedb')
    )

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/users')
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/init-db')
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100)
            )
        """)
        cursor.execute("""
            INSERT INTO users (name, email) VALUES
            ('John Doe', 'john@example.com'),
            ('Jane Smith', 'jane@example.com')
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Database initialized"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.get('/api/time')
def time():
    # Placeholder for actual time fetching logic
    #get server time from db
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message={'time': row[0]})

@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via Testi!'")
    row = cur.fetchone()
    cur.close(); conn.close()
    return jsonify(message=row[0])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
