"""
Demo file containing various Python SAST (Static Application Security Testing) issues.
This file intentionally contains security vulnerabilities for testing purposes.
DO NOT use this code in production!
"""

import os
import pickle
import random
import hashlib
import subprocess
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import sqlite3
import requests
import tempfile
import yaml

# SAST Issue 1: Hardcoded credentials and secrets
DATABASE_PASSWORD = "SuperSecret123!"
API_KEY = "sk-1234567890abcdef1234567890abcdef"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA1234567890\n-----END RSA PRIVATE KEY-----"

# SAST Issue 2: SQL Injection vulnerability
def get_user_by_name(username):
    """Vulnerable to SQL injection"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Direct string concatenation - SQL injection risk
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

def get_user_by_id(user_id):
    """Another SQL injection vulnerability using format strings"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # String formatting - SQL injection risk
    query = "SELECT * FROM users WHERE id = %s" % user_id
    cursor.execute(query)
    return cursor.fetchall()

def search_users(search_term):
    """SQL injection via f-string"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # f-string - SQL injection risk
    query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    return cursor.fetchall()

# SAST Issue 3: Command Injection vulnerabilities
def ping_host(hostname):
    """Vulnerable to command injection"""
    # Shell=True with user input is dangerous
    command = "ping -c 4 " + hostname
    return subprocess.call(command, shell=True)

def list_files(directory):
    """Command injection via os.system"""
    # os.system is vulnerable to command injection
    os.system("ls -la " + directory)

def execute_command(user_command):
    """Direct command execution"""
    # Direct execution of user input
    return os.popen(user_command).read()

# SAST Issue 4: Path Traversal vulnerabilities
def read_user_file(filename):
    """Path traversal vulnerability"""
    # No validation of filename - allows ../../../etc/passwd
    base_path = "/var/www/uploads/"
    file_path = base_path + filename
    with open(file_path, 'r') as f:
        return f.read()

def serve_file(requested_file):
    """Another path traversal issue"""
    # Direct concatenation allows directory traversal
    return open("/app/files/" + requested_file).read()

# SAST Issue 5: Insecure deserialization
def load_user_data(serialized_data):
    """Insecure deserialization using pickle"""
    # pickle.loads() on untrusted data can execute arbitrary code
    return pickle.loads(serialized_data)

def load_config(config_data):
    """Unsafe YAML loading"""
    # yaml.load() without Loader parameter is unsafe
    return yaml.load(config_data)

# SAST Issue 6: Weak cryptography
def hash_password(password):
    """Using weak MD5 hash for passwords"""
    # MD5 is cryptographically broken
    return hashlib.md5(password.encode()).hexdigest()

def encrypt_data(data):
    """Using weak SHA1 hash"""
    # SHA1 is deprecated for security purposes
    return hashlib.sha1(data.encode()).hexdigest()

# SAST Issue 7: Weak random number generation for security
def generate_session_token():
    """Weak random number generation for security token"""
    # random module is not cryptographically secure
    token = ''.join([str(random.randint(0, 9)) for _ in range(32)])
    return token

def generate_password_reset_token():
    """Another weak random token"""
    # Using predictable random for security-sensitive operation
    return random.getrandbits(128)

# SAST Issue 8: XML External Entity (XXE) vulnerabilities
def parse_xml(xml_data):
    """Vulnerable to XXE attacks"""
    # Parsing XML without disabling external entities
    parser = ET.XMLParser()
    tree = ET.fromstring(xml_data, parser=parser)
    return tree

def parse_xml_minidom(xml_string):
    """XXE vulnerability with minidom"""
    # minidom doesn't disable external entities by default
    dom = parseString(xml_string)
    return dom

# SAST Issue 9: Server-Side Request Forgery (SSRF)
def fetch_url(url):
    """SSRF vulnerability - no URL validation"""
    # No validation of URL - can access internal resources
    response = requests.get(url)
    return response.text

def proxy_request(target_url):
    """Another SSRF issue"""
    # User-controlled URL without validation
    return requests.post(target_url, data={'key': 'value'}).json()

# SAST Issue 10: Insecure file permissions
def create_config_file(config_content):
    """Creating file with insecure permissions"""
    filename = '/tmp/config.txt'
    # Creates file with default permissions (might be too permissive)
    with open(filename, 'w') as f:
        f.write(config_content)
    # Setting overly permissive permissions
    os.chmod(filename, 0o777)
    return filename

# SAST Issue 11: Use of assert for security checks
def validate_admin(user_role):
    """Using assert for security validation"""
    # assert statements can be optimized away with -O flag
    assert user_role == "admin", "User must be admin"
    return True

# SAST Issue 12: Insecure temporary file creation
def create_temp_file(data):
    """Insecure temporary file handling"""
    # mktemp is deprecated and insecure (race condition)
    temp_filename = tempfile.mktemp()
    with open(temp_filename, 'w') as f:
        f.write(data)
    return temp_filename

# SAST Issue 13: Eval injection
def calculate(expression):
    """Code injection via eval"""
    # eval() executes arbitrary Python code
    return eval(expression)

def execute_code(code_string):
    """Code injection via exec"""
    # exec() executes arbitrary Python code
    exec(code_string)

# SAST Issue 14: Regular expression DoS (ReDoS)
import re

def validate_email(email):
    """Potentially vulnerable to ReDoS"""
    # Complex regex pattern that could cause ReDoS
    pattern = r'^([a-zA-Z0-9]+([._+-][a-zA-Z0-9]+)*)@([a-zA-Z0-9]+([.-][a-zA-Z0-9]+)*\.[a-zA-Z]{2,})$'
    return re.match(pattern, email)

# SAST Issue 15: Information disclosure
def handle_error(e):
    """Exposing sensitive error information"""
    # Printing full exception details can leak sensitive info
    print(f"Error occurred: {e}")
    print(f"Exception type: {type(e)}")
    import traceback
    traceback.print_exc()

# SAST Issue 16: Insecure SSL/TLS
def fetch_secure_data(url):
    """Disabling SSL verification"""
    # verify=False disables SSL certificate verification
    response = requests.get(url, verify=False)
    return response.text

# SAST Issue 17: Open redirect vulnerability
def redirect_user(redirect_url):
    """Open redirect vulnerability"""
    # No validation of redirect URL
    return f"<meta http-equiv='refresh' content='0; url={redirect_url}'>"

# SAST Issue 18: Mass assignment vulnerability
class User:
    def __init__(self):
        self.username = ""
        self.is_admin = False
        
    def update_from_request(self, request_data):
        """Mass assignment - allows setting any attribute"""
        for key, value in request_data.items():
            # No whitelist - attacker could set is_admin=True
            setattr(self, key, value)

# SAST Issue 19: Logging sensitive data
def login_user(username, password):
    """Logging sensitive information"""
    # Logging passwords is a security issue
    print(f"User login attempt: {username} with password: {password}")
    # More logging issues
    import logging
    logging.info(f"Authentication for {username} with credentials: {password}")

# SAST Issue 20: Using dangerous functions
def process_file(filename):
    """Using deprecated and dangerous functions"""
    # os.tempnam is deprecated and insecure
    temp = os.tempnam('/tmp')
    # input() in Python 2 evaluates code (though this is Python 3)
    return temp

if __name__ == "__main__":
    print("This file contains intentional security vulnerabilities for SAST testing.")
    print("DO NOT use any of this code in production!")
