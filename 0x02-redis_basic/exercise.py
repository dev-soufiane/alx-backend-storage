import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator that counts method calls."""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increments call count and calls method."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that logs method inputs and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Logs inputs and outputs."""
        input_str = str(args)
        self._redis.rpush(f"{method.__qualname__}:inputs", input_str)
        output_str = str(method(self, *args, **kwargs))
        self._redis.rpush(f"{method.__qualname__}:outputs", output_str)
        return output_str

    return wrapper


def replay(fn: Callable):
    """Displays the history of calls of a particular function."""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print(f"{function_name} was called {value} times:")
    inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    outputs = r.lrange(f"{function_name}:outputs", 0, -1)

    for input_data, output_data in zip(inputs, outputs):
        try:
            input_data = input_data.decode("utf-8")
        except Exception:
            input_data = ""

        try:
            output_data = output_data.decode("utf-8")
        except Exception:
            output_data = ""

        print(f"{function_name}(*{input_data}) -> {output_data}")


class Cache:
    """Implements a Redis-based cache."""

    def __init__(self):
        """Initializes Redis client and flushes the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis with a random key and returns the key."""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) ->
    Union[str, bytes, int, float]:
        """Retrieves data from Redis and optionally applies a conversion
        function."""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Retrieves a string value from Redis."""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Retrieves an integer value from Redis."""
        value = self._redis.get(key)
        try:
            return int(value.decode("utf-8"))
        except (ValueError, AttributeError):
            return 0
