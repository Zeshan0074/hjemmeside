from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="98765321",
    database="auth"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['psw']  # Changed from 'password' to 'psw' to match the HTML

    cursor = db.cursor()
    cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
    db.commit()
    cursor.close()

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
