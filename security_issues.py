import sqlite3
import os
import pickle
import subprocess
import hashlib


# SQL Injection vulnerability
def get_user_by_username(username):
    """Fetch user from database - VULNERABLE to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable: direct string concatenation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    
    result = cursor.fetchone()
    conn.close()
    return result


def authenticate_user(username, password):
    """Authenticate user - VULNERABLE to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Vulnerable: string formatting
    query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()
    return user is not None


# Command Injection vulnerability
def ping_host(hostname):
    """Ping a host - VULNERABLE to command injection"""
    # Vulnerable: user input directly in shell command
    command = f"ping -c 4 {hostname}"
    result = os.system(command)
    return result


def check_network(ip_address):
    """Check network connectivity - VULNERABLE to command injection"""
    # Vulnerable: using shell=True with user input
    cmd = f"nslookup {ip_address}"
    output = subprocess.check_output(cmd, shell=True)
    return output.decode()


# Path Traversal vulnerability
def read_user_file(filename):
    """Read a user file - VULNERABLE to path traversal"""
    # Vulnerable: no validation of filename
    base_dir = "/var/www/uploads/"
    file_path = base_dir + filename
    
    with open(file_path, 'r') as f:
        content = f.read()
    return content


def get_log_file(log_name):
    """Get log file contents - VULNERABLE to path traversal"""
    # Vulnerable: user-controlled path
    log_dir = "/var/logs/"
    full_path = os.path.join(log_dir, log_name)
    
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            return f.read()
    return None


# Insecure Deserialization
def load_user_session(session_data):
    """Load user session - VULNERABLE to insecure deserialization"""
    # Vulnerable: pickle can execute arbitrary code
    user_session = pickle.loads(session_data)
    return user_session


# Weak Cryptography
def hash_password(password):
    """Hash password - VULNERABLE uses weak hashing"""
    # Vulnerable: MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()


def generate_token(user_id):
    """Generate auth token - VULNERABLE uses weak hashing"""
    # Vulnerable: SHA1 is considered weak
    return hashlib.sha1(str(user_id).encode()).hexdigest()


# Hardcoded Credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"
SECRET_KEY = "my-super-secret-key-do-not-share"


def connect_to_database():
    """Connect to database with hardcoded credentials"""
    username = "admin"
    password = "password123"  # Hardcoded password
    host = "localhost"
    
    connection_string = f"postgresql://{username}:{password}@{host}/mydb"
    return connection_string


# Unsafe YAML loading
def load_config(yaml_content):
    """Load YAML config - VULNERABLE to code execution"""
    import yaml
    # Vulnerable: yaml.load() can execute arbitrary Python code
    config = yaml.load(yaml_content)
    return config


# Main function to demonstrate the vulnerabilities
if __name__ == "__main__":
    # These functions are reachable and can be called
    print("Security Issues Demo")
    
    # Example calls (commented out to avoid actual execution)
    # user = get_user_by_username("admin")
    # result = ping_host("localhost")
    # content = read_user_file("data.txt")
    # password_hash = hash_password("mypassword")
