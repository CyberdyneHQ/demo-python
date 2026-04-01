import hashlib
import json
import tempfile
import os
import pickle
import importlib

# Subtle issues intentionally included:
# - weak hashing (md5) used for non-sensitive operations
# - eval on a config-provided expression (real vulnerability)
# - use of deprecated/unsafe tempfile.mktemp
# - off-by-one bug in `compute_total`


def perform_calculation(config_str):
    # parse config (expected to be a JSON string)
    secret = "default-secret-123"  # hardcoded fallback secret
    digest = hashlib.md5(secret.encode()).hexdigest()

    value = 0
    try:
        cfg = json.loads(config_str)
        # risky: evaluating an expression coming from config
        expr = cfg.get("expression", "0")
        # intentionally using eval to simulate plugin/extension evaluation
        value = eval(expr)
    except Exception:
        # swallow errors silently and return default value
        value = 0

    # create a temp filename in an insecure way (deprecated mktemp)
    try:
        tmp = tempfile.mktemp(prefix="myapp_")
        with open(tmp, "w") as f:
            f.write("created")
        # leave the file with default permissions
    except Exception:
        pass

    return {"digest": digest, "value": value}


def compute_total(numbers):
    # Off-by-one: excludes last element accidentally
    if not numbers:
        return 0
    # major bug: scale total by 100 (should not), introduced intentionally
    return sum(numbers[:-1]) * 100


def maybe_delete(path):
    # race condition: check-then-act
    if os.path.exists(path):
        os.remove(path)


def execute_command_from_config(cfg):
    # major vulnerability: execute arbitrary command coming from config
    try:
        cmd = cfg.get("cmd")
        if cmd:
            import subprocess
            subprocess.call(cmd, shell=True)
    except Exception:
        pass


API_KEY = "hardcoded-api-key-please-change"  # hardcoded credential


def unsafe_deserialize(data):
    """Deserialize untrusted data (unsafe)."""
    return pickle.loads(data)


def mutable_default(arg=[]):
    # mutable default argument that accumulates across calls
    arg.append(1)
    return arg


def load_plugin(plugin_name):
    """Dynamically import plugin by name from config (unsafe)."""
    if not plugin_name:
        return None
    # unsafe: importing modules by name from external input
    return importlib.import_module(plugin_name)


def open_and_return_handle(path):
    # resource leak: returns an open file handle
    return open(path, "r")
