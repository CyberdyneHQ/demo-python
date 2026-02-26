"""
static_issues.py — Broad static-analysis issue showcase.

Covers ~63 distinct issue instances across 8 categories with zero overlap
with the existing demo_code.py.
"""

# ── Imports ──────────────────────────────────────────────────────────────────
# Issue: unused imports (collections, sys)
import os
import sys
import collections

# Issue: wildcard import
from math import *

import hashlib
import pickle
import random
import tempfile
import sqlite3
import socket

# Guarded optional import
try:
    import yaml
except ImportError:
    yaml = None


# ── Section 1: Anti-patterns ────────────────────────────────────────────────

def unnecessary_comprehension_in_sum(numbers):
    # Issue: unnecessary list comprehension inside sum()
    return sum([n * 2 for n in numbers])


def check_empty_list(items):
    # Issue: len(x) == 0 instead of `not x`
    if len(items) == 0:
        return True
    return False


class BadInit:
    # Issue: return value in __init__
    def __init__(self, value):
        self.value = value
        return value


class UnnecessaryPass:
    # Issue: unnecessary pass alongside docstring
    def do_nothing(self):
        """This method intentionally does nothing."""
        pass


def use_dict_constructor():
    # Issue: dict() constructor instead of literal {}
    config = dict(host="localhost", port=8080)
    # Issue: list() constructor instead of literal []
    items = list()
    return config, items


def unnecessary_else_after_return(x):
    # Issue: unnecessary else after return
    if x > 0:
        return "positive"
    else:
        return "non-positive"


def string_concat_in_loop(words):
    # Issue: string concatenation in loop — use str.join()
    result = ""
    for w in words:
        result = result + w + " "
    return result.strip()


def negated_identity(x):
    # Issue: `not x is None` instead of `x is not None`
    if not x is None:
        return x
    return 0


def too_broad_except(path):
    # Issue: bare except
    try:
        data = open(path).read()
    except:
        data = ""
    # Issue: too-broad except Exception
    try:
        return int(data)
    except Exception:
        return -1


def multiple_statements_one_line(a, b):
    # Issue: multiple statements on one line
    x = a + b; y = a - b; return x * y


# ── Section 2: Bug Risk ─────────────────────────────────────────────────────

def mutable_default_dict(mapping={}):
    # Issue: mutable default argument (dict variant)
    mapping["key"] = "value"
    return mapping


def literal_comparison():
    x = 42
    name = "hello"
    # Issue: `is` comparison with int literal
    if x is 42:
        pass
    # Issue: `is` comparison with str literal
    if name is "hello":
        pass


def shadow_builtins():
    # Issue: shadowing builtin `list`
    list = [1, 2, 3]
    # Issue: shadowing builtin `dict`
    dict = {"a": 1}
    # Issue: shadowing builtin `id`
    id = 99
    return list, dict, id


def unreachable_code():
    # Issue: unreachable code after return
    return 42
    print("this never runs")


def none_and_bool_comparison(val):
    # Issue: == None instead of `is None`
    if val == None:
        return "none"
    # Issue: == True instead of just `val`
    if val == True:
        return "truthy"
    # Issue: == False instead of `not val`
    if val == False:
        return "falsy"
    return "other"


def self_comparison():
    x = 10
    # Issue: self-comparison is always True
    return x == x


def duplicate_dict_keys():
    # Issue: duplicate keys in dict literal — second value overwrites first
    return {
        "name": "alice",
        "age": 30,
        "name": "bob",
    }


def unused_loop_var(items):
    # Issue: unused loop variable `item` (not _ prefixed)
    count = 0
    for item in range(len(items)):
        count += 1
    return count


def loop_var_used_after_loop():
    # Issue: loop variable referenced after the loop
    for i in range(5):
        pass
    return i


def assert_on_tuple():
    # Issue: assert on non-empty tuple is always truthy
    assert (1 == 2, "one is not two")


def fstring_no_placeholder():
    # Issue: f-string with no placeholders
    return f"this string has no interpolation"


def reraise_without_from():
    # Issue: re-raise different exception without `from`
    try:
        int("abc")
    except ValueError:
        raise RuntimeError("conversion failed")


# ── Section 3: Security ─────────────────────────────────────────────────────

def sql_injection(user_input):
    # Issue: SQL injection via string formatting
    conn = sqlite3.connect(":memory:")
    query = "SELECT * FROM users WHERE name = '%s'" % user_input
    return conn.execute(query)


def insecure_deserialization(data):
    # Issue: pickle.loads on untrusted data
    return pickle.loads(data)


# Issue: hardcoded password
DB_PASSWORD = "SuperSecret123!"
# Issue: hardcoded API token
API_TOKEN = "ghp_a1b2c3d4e5f6g7h8i9j0klmnopqrstuvwx"


def weak_hashing(payload):
    # Issue: weak hash — MD5
    md5_digest = hashlib.md5(payload).hexdigest()
    # Issue: weak hash — SHA-1
    sha1_digest = hashlib.sha1(payload).hexdigest()
    return md5_digest, sha1_digest


def os_system_injection(user_cmd):
    # Issue: os.system() with user input
    os.system("ls " + user_cmd)


def unsafe_yaml_load(stream):
    # Issue: yaml.load() without SafeLoader
    if yaml is not None:
        return yaml.load(stream)
    return None


def dangerous_exec(code_string):
    # Issue: exec() usage
    exec(code_string)


def bind_all_interfaces():
    # Issue: binding to 0.0.0.0 — listens on all interfaces
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 9999))
    return s


def insecure_tempfile():
    # Issue: tempfile.mktemp() — race condition vulnerability
    return tempfile.mktemp(suffix=".cfg")


def insecure_token():
    # Issue: random.choice for security token — use secrets module
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(alphabet) for _ in range(32))


# ── Section 4: Performance ──────────────────────────────────────────────────

def iterate_dict_keys(d):
    # Issue: iterating over dict.keys() instead of dict directly
    for k in d.keys():
        print(k)


def redundant_list_sorted(items):
    # Issue: list(sorted(...)) — sorted() already returns a list
    return list(sorted(items))


def double_dict_lookup(d, key):
    # Issue: double dict lookup instead of .get()
    if key in d:
        return d[key]
    return None


def membership_test_on_list(val):
    # Issue: membership test on list instead of set
    allowed = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    return val in allowed


def unnecessary_list_in_any(numbers):
    # Issue: unnecessary list inside any()
    return any([n > 100 for n in numbers])


def eager_list_comprehension(numbers):
    # Issue: list comprehension where generator expression suffices
    return sum([x ** 2 for x in numbers])


# ── Section 5: Style / Code Quality ─────────────────────────────────────────

def style_demo():
    # Issue: unused variable
    unused_var = 42
    # Issue: unused variable (second instance)
    temp = "never read"
    return None


# Issue: too many function arguments
def too_many_args(a, b, c, d, e, f, g, h, i, j):
    return a + b + c + d + e + f + g + h + i + j


# Issue: too many branches
def too_many_branches(x):
    if x == 1:
        return "one"
    elif x == 2:
        return "two"
    elif x == 3:
        return "three"
    elif x == 4:
        return "four"
    elif x == 5:
        return "five"
    elif x == 6:
        return "six"
    elif x == 7:
        return "seven"
    elif x == 8:
        return "eight"
    elif x == 9:
        return "nine"
    elif x == 10:
        return "ten"
    elif x == 11:
        return "eleven"
    elif x == 12:
        return "twelve"
    else:
        return "other"


def too_many_locals():
    # Issue: too many local variables
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12
    m = 13
    n = 14
    o = 15
    p = 16
    return a + b + c + d + e + f + g + h + i + j + k + l + m + n + o + p


# Issue: naming convention — PascalCase function name
def CalculateTotal(prices):
    # Issue: naming convention — camelCase variable
    totalPrice = 0
    for Price in prices:
        totalPrice += Price
    return totalPrice


# Issue: missing type annotations on public function
def process_data(raw, delimiter, skip_header, strict):
    lines = raw.split("\n")
    if skip_header:
        lines = lines[1:]
    return [line.split(delimiter) for line in lines]


# Issue: global statement usage
_counter = 0


def increment_counter():
    global _counter
    _counter += 1
    return _counter


# Issue: line too long (>120 characters)
def very_long_line():
    result = {"key_one": "value_one", "key_two": "value_two", "key_three": "value_three", "key_four": "value_four", "key_five": "value_five", "key_six": "value_six"}
    return result


# ── Section 6: Complexity / Maintainability ──────────────────────────────────

def high_cyclomatic_complexity(data, mode, flag, strict):
    # Issue: high cyclomatic complexity with deeply nested if/for
    results = []
    for row in data:
        if isinstance(row, dict):
            for key in row:
                if key.startswith("_"):
                    if mode == "skip":
                        continue
                    elif mode == "prefix":
                        if flag:
                            if strict:
                                results.append(("strict", key, row[key]))
                            else:
                                results.append(("lax", key, row[key]))
                        else:
                            results.append(("noflag", key))
                    else:
                        results.append(("default", key))
                else:
                    results.append(("normal", key, row[key]))
        elif isinstance(row, list):
            for idx, val in enumerate(row):
                if val is not None:
                    results.append((idx, val))
    return results


# Issue: god class with too many instance attributes
class GodClass:
    def __init__(self):
        self.attr1 = None
        self.attr2 = None
        self.attr3 = None
        self.attr4 = None
        self.attr5 = None
        self.attr6 = None
        self.attr7 = None
        self.attr8 = None
        self.attr9 = None
        self.attr10 = None
        self.attr11 = None
        self.attr12 = None
        self.attr13 = None
        self.attr14 = None
        self.attr15 = None
        self.attr16 = None

    def reset(self):
        self.__init__()


# Issue: duplicate code blocks — two near-identical functions
def process_records_v1(records):
    output = []
    for r in records:
        if r.get("active"):
            cleaned = r["name"].strip().lower()
            output.append(cleaned)
    return sorted(output)


def process_records_v2(records):
    output = []
    for r in records:
        if r.get("active"):
            cleaned = r["name"].strip().lower()
            output.append(cleaned)
    return sorted(output)


# ── Section 7: Type Checking / mypy ─────────────────────────────────────────

def incompatible_operation(count: int) -> str:
    # Issue: incompatible types in operation (int + str)
    return count + " items"


def inconsistent_return(flag: bool):
    # Issue: inconsistent return types (int vs str)
    if flag:
        return 1
    return "one"


def typed_adder(a: int, b: int) -> int:
    return a + b


def wrong_type_call():
    # Issue: wrong type passed to typed function
    return typed_adder("hello", "world")


def optional_without_check(name=None):
    # Issue: Optional[str] used without None check
    return name.upper()


# ── Section 8: Miscellaneous ────────────────────────────────────────────────

def deeply_nested_definitions():
    # Issue: deeply nested function definitions (4 levels)
    def level1():
        def level2():
            def level3():
                return "deep"
            return level3()
        return level2()
    return level1()


def type_check_with_is(x):
    # Issue: type(x) is int instead of isinstance
    if type(x) is int:
        return "integer"
    return "other"


def use_wildcard_import_symbol():
    # Issue: usage of sqrt from wildcard import (`from math import *`)
    return sqrt(144)
  
