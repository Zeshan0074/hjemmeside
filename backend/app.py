from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Configure MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="auth"
    )

@app.route('/')
def index():
    return "Welcome to the API"

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400

    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user:
                return jsonify({'status': 'error', 'message': 'Email already exists'}), 400
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
            db.commit()
        
        return jsonify({'status': 'success'}), 200
    except Error as err:
        return jsonify({'status': 'error', 'message': str(err)}), 500
    finally:
        if db.is_connected():
            db.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    try:
        db = get_db_connection()
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (username,))
            user = cursor.fetchone()
            
            if not user:
                return jsonify({'status': 'error', 'message': 'User does not exist'}), 404

            stored_password = user[2]  # Assuming the password is the third column in the table

            if stored_password == password:
                return jsonify({'status': 'success'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Wrong password'}), 401

    except Error as err:
        return jsonify({'status': 'error', 'message': str(err)}), 500
    finally:
        if db.is_connected():
            db.close()

if __name__ == "__main__":
    app.run(debug=True)
