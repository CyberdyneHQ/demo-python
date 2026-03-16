"""
Test file with modern Python 3.10+ syntax that might be incorrectly flagged.
"""
from typing import TypeAlias


# Python 3.10+ structural pattern matching (match/case)
def process_command(command: dict):
    """Using match/case statements - new in Python 3.10"""
    match command:
        case {"action": "start", "target": target}:
            return f"Starting {target}"
        case {"action": "stop", "target": target}:
            return f"Stopping {target}"
        case {"action": "restart", "target": target}:
            return f"Restarting {target}"
        case _:
            return "Unknown command"


# Python 3.10+ union type syntax with |
def process_value(value: int | str | None) -> str:
    """Using | for union types instead of Union"""
    if value is None:
        return "None"
    return str(value)


# Python 3.9+ dict merge operator
def merge_configs(base: dict, override: dict) -> dict:
    """Using | operator for dict merging - new in Python 3.9"""
    return base | override


# Python 3.9+ type hints with built-in collections
def get_items(data: list[str]) -> dict[str, int]:
    """Using lowercase list/dict in type hints - new in Python 3.9"""
    return {item: len(item) for item in data}


# Python 3.10+ TypeAlias
UserID: TypeAlias = int | str


def get_user(user_id: UserID) -> dict:
    """Using TypeAlias - new in Python 3.10"""
    return {"id": user_id, "name": "User"}


# Python 3.11+ Self type
from typing import Self


class Builder:
    """Using Self type hint - new in Python 3.11"""
    
    def __init__(self):
        self.value = 0
    
    def add(self, n: int) -> Self:
        """Return Self instead of 'Builder'"""
        self.value += n
        return self
    
    def multiply(self, n: int) -> Self:
        """Chainable method using Self"""
        self.value *= n
        return self


# Python 3.11+ exception groups
def process_multiple_operations():
    """Using ExceptionGroup - new in Python 3.11"""
    errors = []
    
    try:
        operation1()
    except Exception as e:
        errors.append(e)
    
    try:
        operation2()
    except Exception as e:
        errors.append(e)
    
    if errors:
        raise ExceptionGroup("Multiple operations failed", errors)


def operation1():
    """Dummy operation"""
    pass


def operation2():
    """Dummy operation"""
    pass


if __name__ == "__main__":
    cmd = {"action": "start", "target": "server"}
    print(process_command(cmd))
    
    print(process_value(42))
    print(process_value("hello"))
    print(process_value(None))
    
    config = merge_configs({"a": 1}, {"b": 2})
    print(config)
    
    items = get_items(["hello", "world"])
    print(items)
    
    builder = Builder().add(5).multiply(2)
    print(builder.value)
