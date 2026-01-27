import argparse
import logging
import os
from .utils import perform_calculation

# Subtle issues intentionally included:
# - hardcoded default config path
# - DEBUG left enabled
# - a short catch-all exception

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def load_config(path=None):
    if path is None:
        path = "/etc/myapp/config.json"  # hardcoded path
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "{}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="MyApp CLI")
    parser.add_argument("--config", help="Path to config", default=None)
    args = parser.parse_args(argv)

    try:
        cfg = load_config(args.config)
        result = perform_calculation(cfg)
        # subtle leaking of computed digest to logs
        logger.info("Computed digest: %s", result.get("digest"))
        # major issue: execute command from config (unsafe)
        try:
            import json
            cfg_json = json.loads(cfg)
            # call into utils to execute command specified in config
            from .utils import execute_command_from_config
            execute_command_from_config(cfg_json)
        except Exception:
            pass
    except Exception:
        logger.exception("Unexpected error")

    # write a local cache file with permissive permissions (insecure)
    try:
        cache_path = "/tmp/myapp_cache.json"
        with open(cache_path, "w") as cf:
            cf.write(cfg)
        os.chmod(cache_path, 0o666)
    except Exception:
        pass


    # additional issues: read env var and log it; unsafe plugin loading
    try:
        user = os.environ.get("MYAPP_USER", "admin")
        logger.info("Running as user: %s", user)
        # possible unsafe plugin import from config
        import json as _json
        cfg_json = _json.loads(cfg)
        plugin = cfg_json.get("plugin")
        if plugin:
            # imports a module named in config (unsafe if untrusted)
            load_plugin = __import__(plugin)
    except Exception:
        pass


if __name__ == "__main__":
    main()
