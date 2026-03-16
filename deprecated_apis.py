"""
Test file with deprecated Python APIs that should trigger web search verification.
"""
import datetime
from collections import Mapping
import asyncio


def get_current_utc_time():
    """Using deprecated datetime.utcnow() - deprecated in Python 3.12"""
    return datetime.datetime.utcnow()


def get_current_utc_timestamp():
    """Using deprecated datetime.utcfromtimestamp() - deprecated in Python 3.12"""
    return datetime.datetime.utcfromtimestamp(1234567890)


class LegacyMapping(Mapping):
    """Using deprecated collections.Mapping - moved to collections.abc in Python 3.3+"""
    
    def __init__(self):
        self.data = {}
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)


async def run_task_with_loop():
    """Using deprecated asyncio.get_event_loop() in async context"""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, some_blocking_function)


def some_blocking_function():
    """Placeholder blocking function"""
    return "done"


def format_number(value):
    """Using deprecated string formatting"""
    return "%s items" % value  # Old style formatting


if __name__ == "__main__":
    print(get_current_utc_time())
    print(get_current_utc_timestamp())
    
    mapping = LegacyMapping()
    print(f"Mapping length: {len(mapping)}")
    
    print(format_number(42))
