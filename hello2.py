import os
import sys
import json  # unused import
import subprocess
import pickle
import yaml
import tempfile

# Missing docstring for module

# Hardcoded credentials - security issue
API_KEY = "your-api-key-here-12345"  # hardcoded credential
PASSWORD = "admin123"
DATABASE_URL = "postgresql://user:password@localhost:5432/db"

def badFunction(x,y):  # non-standard naming, missing spaces
    # Missing docstring
    result=x+y  # missing spaces around operator
    print(result)
    return result

class myClass:  # non-standard class naming
    def __init__(self):
        self.value = 0
    
    def do_something(self, a, b):
        # Undefined variable
        c = a + b + undefined_var
        return c

def divide_numbers(a, b):
    # Division by zero not handled
    return a / b

def unused_function():
    pass

# Variable shadowing
list = [1, 2, 3]  # shadows built-in

# Bare except clause
try:
    x = 1 / 0
except:  # bare except
    pass

# Comparison with singleton
if x == None:  # should use 'is None'
    print("x is None")

# Mutable default argument
def append_to_list(item, my_list=[]):
    my_list.append(item)
    return my_list

# Unused variable
def calculate():
    unused = 42
    result = 10 + 20
    return result

# Multiple statements on one line
a = 1; b = 2; c = 3

# Line too long (if you have line length rules)
very_long_variable_name = "This is a very long string that exceeds the typical 80 or 100 character limit for Python code style guides and will be flagged by most linters"

# Redefined outer name
def outer():
    x = 1
    def inner():
        x = 2  # redefines outer x
        return x
    return inner()

# String formatting issues
name = "World"
message = "Hello " + name + "!"  # should use f-strings or .format()

# SQL Injection vulnerability
def get_user(username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return query

# Command injection vulnerability
def run_command(user_input):
    os.system("ls " + user_input)  # shell injection
    subprocess.call("cat " + user_input, shell=True)  # shell injection

# Path traversal vulnerability
def read_file(filename):
    with open("/var/data/" + filename, "r") as f:  # no path validation
        return f.read()

# Insecure deserialization
def load_data(serialized_data):
    return pickle.loads(serialized_data)  # pickle is unsafe

# Weak cryptography
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is weak

# Insecure temporary file
def create_temp():
    filename = tempfile.mktemp()  # insecure, use mkstemp instead
    return filename

# YAML unsafe load
def load_config(yaml_string):
    return yaml.load(yaml_string)  # should use safe_load

# eval() usage - arbitrary code execution
def calculate_expression(expr):
    return eval(expr)  # dangerous!

# Assert used for validation
def validate_age(age):
    assert age > 0  # asserts can be disabled with -O flag
    return True

if __name__ == "__main__":
    badFunction(1,2)
    print(list)
    print(API_KEY)  # exposing secret
