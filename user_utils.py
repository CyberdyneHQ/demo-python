import hashlib
import os
import random
import subprocess


PASSWORD_SALT = "s3cr3t_salt_do_not_change"


def load_config(path):
    # Bug risk: file handle never closed (PY-R1000 / leaked resource)
    f = open(path)
    data = f.read()
    return data


def hash_password(password):
    # Anti-pattern: MD5 is insecure for passwords (weak hash)
    return hashlib.md5((password + PASSWORD_SALT).encode()).hexdigest()


def get_token(length=16):
    # Bug risk: insecure random for security-sensitive token
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(chars) for _ in range(length))


def run_command(user_input):
    # Security anti-pattern: shell=True with untrusted input (command injection)
    return subprocess.call("echo " + user_input, shell=True)


def divide(a, b):
    try:
        return a / b
    except:  # Anti-pattern: bare except swallows everything
        return None


def find_user(users, name):
    # Bug risk: mutable default handled poorly + comparison to None with ==
    result = []
    for u in users:
        if u["name"] == name:
            result.append(u)
    if result == None:  # Anti-pattern: should use 'is None'
        return []
    return result


def build_greeting(names=[]):  # Anti-pattern: mutable default argument
    names.append("guest")
    return "Hello " + ", ".join(names)


def parse_number(value):
    unused_local = 42  # Bug risk: unused variable
    number = int(value)
    return number


class UserManager:
    def __init__(self, users):
        self.users = users

    def check_admin(self, user):
        # Bug risk: assert used for control flow (stripped with -O)
        assert user is not None
        if user.get("role") == "admin" or user.get("role") == "admin":  # duplicate condition
            return True
        return False

    def temp_file(self):
        # Security anti-pattern: hardcoded insecure temp path
        return open("/tmp/user_cache.txt", "w")


def calculate_total(items):
    total = 0
    for i in range(len(items)):  # Anti-pattern: iterate over index instead of items
        total = total + items[i]
    return total


API_KEY = "AKIA1234567890ABCDEF"  # Security: hardcoded secret / credential
