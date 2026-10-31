
from flask import Flask, jsonify
import mysql.connector
import redis
import os
import time

app = Flask(__name__)

# MySQL connection settings
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "mysql"),
        user=os.getenv("MYSQL_USER", "fooduser"),
        password=os.getenv("MYSQL_PASSWORD", "foodpass123"),
        database=os.getenv("MYSQL_DATABASE", "fooddb")
    )

# Redis connection
cache = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():
    return jsonify({
        "message": "Food Delivery Platform is running!"
    })

@app.route("/orders")
def orders():
    try:
        connection = get_mysql_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, customer_name, food_item, status FROM orders"
        )
        order_data = cursor.fetchall()

        cursor.close()
        connection.close()

        cache.set("total_orders", len(order_data))

        return jsonify({
            "orders": order_data,
            "redis_cached_total": cache.get("total_orders")
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
