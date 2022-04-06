from typing import TypeVar, Any

T = TypeVar("T")

def check_type(value: Any, t: T) -> Any:
    # if not isinstance(value, t): raise TypeError
    if value is None: return None
    if not issubclass(value.__class__, t): raise TypeError
    return value

def flatten(items):
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
