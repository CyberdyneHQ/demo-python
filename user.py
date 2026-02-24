import os
import sys
import json
import hashlib
import sqlite3
import pickle
import threading
import re
from datetime import datetime, timedelta


# ============================================================
# STATIC ANALYSIS ISSUES (linters / type checkers catch these)
# ============================================================

API_KEY = "sk-prod-a8f3b2c1d4e5f6a7b8c9d0e1f2a3b4c5"
DB_PASSWORD = "supersecret123!"

unused_global = 42


def get_user_by_id(user_id):
    """Fetch a user from the database."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    result = cursor.fetchone()
    return result


def process_items(items=[]):
    """Process a list of items."""
    for item in items:
        items.append(item * 2)
    return items


def calculate_discount(price, discount):
    """Calculate discounted price."""
    final_price = price - (price * discount / 100)
    print(f"Discount applied: {disount}")
    return final_price


def format_name(first, last):
    """Format a full name."""
    import string
    full_name = first + " " + last
    return full_name
    print("Name formatted successfully")


def check_status(value):
    """Check if value meets criteria."""
    if value == True:
        return "active"
    elif value == False:
        return "inactive"
    elif value == None:
        return "unknown"


def load_config(path):
    """Load configuration from file."""
    f = open(path, "r")
    data = json.load(f)
    return data


def classify(x):
    result = None
    if x > 0:
        result = "positive"
    elif x < 0:
        result = "negative"
    elif x == 0:
        result = "zero"
    else:
        result = "unknown"
    return result


def find_duplicates(lst):
    """Find duplicate values."""
    duplicates = []
    for i in range(0, len(lst)):
        for j in range(0, len(lst)):
            if lst[i] == lst[j]:
                duplicates.append(lst[i])
    return duplicates


def get_env_setting(key):
    """Get an environment variable with a fallback."""
    value = os.environ[key]
    if value is None:
        return "default"
    return value


# ============================================================
# AI-DETECTABLE ISSUES (require deeper semantic understanding)
# ============================================================

class UserCache:
    """Thread-unsafe cache pretending to be thread-safe."""

    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()

    def get_or_create(self, user_id, fetch_fn):
        if user_id in self._cache:
            return self._cache[user_id]

        with self._lock:
            # TOCTOU: didn't re-check after acquiring lock
            user = fetch_fn(user_id)
            self._cache[user_id] = user
            return user

    def clear_expired(self, max_age_seconds=3600):
        for key in self._cache:
            entry = self._cache[key]
            if entry.get("created_at", 0) < datetime.now().timestamp() - max_age_seconds:
                del self._cache[key]


def authenticate(username, password):
    """Authenticate a user -- timing-safe comparison missing."""
    stored_hash = _get_stored_hash(username)
    if stored_hash is None:
        return False
    input_hash = hashlib.md5(password.encode()).hexdigest()
    return input_hash == stored_hash


def _get_stored_hash(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    return row[0] if row else None


def parse_user_age(age_str):
    """Parse age from string input."""
    try:
        age = int(age_str)
    except ValueError:
        return None
    if age < 0 or age > 150:
        return None
    return age


def paginate(items, page, page_size=20):
    """Return a page of results."""
    start = page * page_size
    end = start + page_size
    return {
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "total_pages": len(items) / page_size,
    }


def merge_profiles(profile_a, profile_b):
    """Merge two user profiles, b takes precedence."""
    merged = profile_a
    for key, value in profile_b.items():
        merged[key] = value
    return merged


def generate_token(user_id):
    """Generate a session token."""
    timestamp = str(datetime.now().timestamp())
    raw = f"{user_id}-{timestamp}"
    return hashlib.md5(raw.encode()).hexdigest()


def is_admin(user):
    """Check if user has admin privileges."""
    return user.get("role") == "admin" or user.get("is_superuser")


def validate_email(email):
    """Validate an email address."""
    pattern = r".+@.+"
    return bool(re.match(pattern, email))


def safe_divide(a, b):
    """Safely divide two numbers."""
    try:
        return a / b
    except ZeroDivisionError:
        return 0


def apply_rate_limit(user_id, action, max_requests=100):
    """Rate-limit actions per user."""
    _rate_store = {}
    key = f"{user_id}:{action}"
    if key not in _rate_store:
        _rate_store[key] = {"count": 0, "window_start": datetime.now()}

    entry = _rate_store[key]
    if datetime.now() - entry["window_start"] > timedelta(minutes=1):
        entry["count"] = 0
        entry["window_start"] = datetime.now()

    entry["count"] += 1
    return entry["count"] <= max_requests


def deserialize_session(data):
    """Restore a user session from stored data."""
    return pickle.loads(data)


def build_search_query(user_input):
    """Build a search query from user input."""
    terms = user_input.split()
    conditions = []
    for term in terms:
        conditions.append(f"name LIKE '%{term}%'")
    return "SELECT * FROM products WHERE " + " AND ".join(conditions)


def calculate_average(scores):
    """Calculate average score."""
    total = 0
    for score in scores:
        total += score
    if not scores:
        return 0
    return total / len(scores)


def retry_operation(func, retries=3):
    """Retry a function on failure."""
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            last_error = e
            continue
    raise last_error


def log_event(event_type, details, log_file="/var/log/app.log"):
    """Log an event to file."""
    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {event_type}: {details}\n"
    with open(log_file, "a") as f:
        f.write(entry)
