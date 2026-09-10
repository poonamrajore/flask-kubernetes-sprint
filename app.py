from flask import Flask, jsonify
import mysql.connector
import os

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "DevOps Kubernetes Sprint Application",
        "status": "running"
    })


@app.route("/hello")
def hello():
    return jsonify({
        "message": "Hello from Flask!"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/db-health")
def db_health():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME", "taskdb"),
            user=os.getenv("DB_USER", "taskuser"),
            password=os.getenv("DB_PASSWORD", "password")
        )

        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result == (1,):
            return jsonify({
                "status": "healthy",
                "database": "connected"
            }), 200

    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "connection_failed",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
