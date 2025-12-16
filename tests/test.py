from flask import Flask, jsonify
import mysql.connector
import time

app = Flask(__name__)

@app.route('/health')
def health():
    """Basic health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/health/ready')
def readiness():
    """Readiness check - varmistaa että sovellus on valmis"""
    try:
        # Testaa database-yhteys
        conn = mysql.connector.connect(
            host='mysql',
            user='myapp',
            password='password',
            database='myapp_db'
        )
        conn.close()

        return jsonify({
            'status': 'ready',
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'not ready',
            'error': str(e)
        }), 503

@app.route('/health/live')
def liveness():
    """Liveness check - varmistaa että sovellus pyörii"""
    return jsonify({'status': 'alive'}), 200
