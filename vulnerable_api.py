"""
Vulnerable Flask API demonstrating common security issues
"""
from flask import Flask, request, jsonify, send_file
import sqlite3
import os
import subprocess
import hashlib
import pickle
import base64

app = Flask(__name__)

# Hardcoded secret key
app.secret_key = "hardcoded-secret-key-12345"

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                     (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)''')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'admin@example.com')")
    conn.commit()
    conn.close()


@app.route('/api/user/<username>')
def get_user(username):
    """SQL Injection vulnerability - username from URL"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: SQL injection via string formatting
    query = f"SELECT username, email FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/login', methods=['POST'])
def login():
    """SQL Injection vulnerability in login"""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: SQL injection
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({'success': True, 'message': 'Login successful'})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401


@app.route('/api/ping')
def ping():
    """Command Injection vulnerability"""
    host = request.args.get('host', 'localhost')
    
    # VULNERABLE: Command injection via os.system
    result = os.system(f"ping -c 2 {host}")
    
    return jsonify({'host': host, 'result': result})


@app.route('/api/dns-lookup')
def dns_lookup():
    """Command Injection via subprocess"""
    domain = request.args.get('domain', '')
    
    # VULNERABLE: Command injection with shell=True
    try:
        output = subprocess.check_output(f"nslookup {domain}", shell=True, stderr=subprocess.STDOUT)
        return jsonify({'domain': domain, 'output': output.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/file/<path:filename>')
def read_file(filename):
    """Path Traversal vulnerability"""
    # VULNERABLE: No path validation, allows directory traversal
    base_path = '/var/www/uploads/'
    file_path = base_path + filename
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download')
def download_file():
    """Path Traversal via send_file"""
    filename = request.args.get('file', '')
    
    # VULNERABLE: User-controlled file path
    file_path = f"/var/www/files/{filename}"
    
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@app.route('/api/session/load', methods=['POST'])
def load_session():
    """Insecure Deserialization vulnerability"""
    data = request.get_json()
    session_data = data.get('session', '')
    
    # VULNERABLE: pickle deserialization of user data
    try:
        decoded = base64.b64decode(session_data)
        session = pickle.loads(decoded)
        return jsonify({'session': session})
    except Exception as e:
        return jsonify({'error': 'Invalid session data'}), 400


@app.route('/api/hash-password')
def hash_password():
    """Weak Cryptography - MD5 for password hashing"""
    password = request.args.get('password', '')
    
    # VULNERABLE: MD5 is cryptographically broken
    hashed = hashlib.md5(password.encode()).hexdigest()
    
    return jsonify({'password': password, 'hash': hashed})


@app.route('/api/eval', methods=['POST'])
def eval_expression():
    """Code Injection via eval()"""
    data = request.get_json()
    expression = data.get('expression', '')
    
    # VULNERABLE: eval allows arbitrary code execution
    try:
        result = eval(expression)
        return jsonify({'expression': expression, 'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/exec', methods=['POST'])
def exec_code():
    """Code Injection via exec()"""
    data = request.get_json()
    code = data.get('code', '')
    
    # VULNERABLE: exec allows arbitrary code execution
    try:
        exec(code)
        return jsonify({'message': 'Code executed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/debug-info')
def debug_info():
    """Information Disclosure - exposes sensitive debug info"""
    # VULNERABLE: Exposes sensitive system information
    return jsonify({
        'environment': dict(os.environ),
        'secret_key': app.secret_key,
        'debug': app.debug,
        'database_password': 'db_password_12345'
    })


if __name__ == '__main__':
    init_db()
    # VULNERABLE: Debug mode enabled and listening on all interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)
