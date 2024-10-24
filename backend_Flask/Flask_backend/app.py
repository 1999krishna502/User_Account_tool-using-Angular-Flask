import os
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('auth.db')
    print("Opened database successfully")
    
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT,number TEXT, password TEXT)')
   
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT,
            password TEXT
        )
    ''')
   
    print('Database tables created successfully')
    conn.close()


init_sqlite_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    username = data.get('username')
    email = data.get('email')
    number = data.get('number')
    password = data.get('password')
    
   

    if not all([username, email,number, password]):
        return jsonify({'error': 'All fields are required!'}), 400
    
     # Check if the username or email already exists
    with sqlite3.connect('auth.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({'error': 'Email is already registered!'}), 400
        
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({'error': 'Username is already taken!'}), 400

    hashed_password = generate_password_hash(password)

    try:
        with sqlite3.connect('auth.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, email, number, password) VALUES (?, ?, ?, ?)",
                        (username, email, number,hashed_password))
            con.commit()
            return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error occurred in registration'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Debugging print statements
    print(f"Received email: {email} and password: {password}")

    # Input validation
    if not all([email, password]):
        return jsonify({'error': 'Email and password are required!'}), 400

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({'error': 'Invalid input data type!'}), 400

    with sqlite3.connect('auth.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

        # Debugging print statement
        print(f"Retrieved user: {user}")

        if user and check_password_hash(user[4], password):  # assuming password hash is in the 4th index
            session['user_id'] = user[0]
            return jsonify({'message': 'Login successful!', 'userId': user[0]}), 200

        else:
            return jsonify({'error': 'Invalid email or password!'}), 401
        
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        with sqlite3.connect('auth.db') as con:
            cur = con.cursor()
            cur.execute("SELECT id, username, email, number FROM users WHERE id=?", (user_id,))
            user = cur.fetchone()

            if user:
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'number': user[3]
                }
                return jsonify(user_data), 200
            else:
                return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error occurred while fetching user data'}), 500
    


@app.route('/api/admin/register', methods=['POST'])
def admin_register():
    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return jsonify({'error': 'All fields are required!'}), 400

    with sqlite3.connect('auth.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM admins WHERE email=?", (email,))
        existing_admin = cur.fetchone()

        if existing_admin:
            return jsonify({'error': 'Email is already registered!'}), 400

        cur.execute("SELECT * FROM admins WHERE username=?", (username,))
        existing_admin = cur.fetchone()

        if existing_admin:
            return jsonify({'error': 'Username is already taken!'}), 400

    hashed_password = generate_password_hash(password)

    try:
        with sqlite3.connect('auth.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO admins (username, email, password) VALUES (?, ?, ?)",
                        (username, email, hashed_password))
            con.commit()
            return jsonify({'message': 'Admin registered successfully!'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error occurred in registration'}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Email and password are required!'}), 400

    with sqlite3.connect('auth.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM admins WHERE email=?", (email,))
        admin = cur.fetchone()

        if admin and check_password_hash(admin[3], password):  # assuming password hash is in the 3rd index
            session['admin_id'] = admin[0]
            return jsonify({'message': 'Admin login successful!', 'adminId': admin[0]}), 200
        else:
            return jsonify({'error': 'Invalid email or password!'}), 401

@app.route('/api/admin/<int:admin_id>', methods=['GET'])
def get_admin(admin_id):
    try:
        with sqlite3.connect('auth.db') as con:
            cur = con.cursor()
            cur.execute("SELECT id, username, email FROM admins WHERE id=?", (admin_id,))
            admin = cur.fetchone()

            if admin:
                admin_data = {
                    'id': admin[0],
                    'username': admin[1],
                    'email': admin[2]
                }
                return jsonify(admin_data), 200
            else:
                return jsonify({'error': 'Admin not found'}), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Error occurred while fetching admin data'}), 500
    

from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message  # Assuming you are using Flask-Mail

# Initialize mail settings (you need to configure these according to your email provider)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'akkunni222@gmail.com'
app.config['MAIL_PASSWORD'] = 'oilc awmb hghi jbqw'  # or app-specific password if 2FA is enabled
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


mail = Mail(app)

# Generate and send a token
def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt=app.secret_key)

def send_password_reset_email(email):
    token = generate_password_reset_token(email)
    # Change the reset_url to point to your Angular frontend
    reset_url = f'http://localhost:4200/reset-password/{token}'
    msg = Message('Password Reset Request', sender='noreply@yourapp.com', recipients=[email])
    msg.body = f'To reset your password, visit the following link: {reset_url}'
    mail.send(msg)


@app.route('/api/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required!'}), 400

    with sqlite3.connect('auth.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()

        if user:
            send_password_reset_email(email)
            return jsonify({'message': 'Password reset email sent!'}), 200
        else:
            return jsonify({'error': 'Email not found!'}), 404


@app.route('/api/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        serializer = URLSafeTimedSerializer(app.secret_key)
        email = serializer.loads(token, salt=app.secret_key, max_age=3600)  # Token valid for 1 hour
    except Exception as e:
        print(f"Token validation error: {e}")
        return jsonify({'error': 'Invalid or expired token!'}), 400

    data = request.json
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'New password is required!'}), 400

    hashed_password = generate_password_hash(new_password)

    try:
        with sqlite3.connect('auth.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET password=? WHERE email=?", (hashed_password, email))
            if cur.rowcount == 0:
                return jsonify({'error': 'Email not found!'}), 404
            con.commit()
    except Exception as e:
        print(f"Database update error: {e}")
        return jsonify({'error': 'Error occurred while updating the password'}), 500

    return jsonify({'message': 'Password reset successfully!'}), 200




if __name__ == '__main__':
    app.run(debug=True)
