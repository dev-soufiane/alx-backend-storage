#!/usr/bin/env python3
import redis
from typing import Union, Optional, Callable
from uuid import uuid4
import sys
from functools import wraps

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts method calls.

    Args:
        method: The method being decorated.

    Returns:
        The wrapped method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Increments call count and calls method """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that logs method inputs and outputs in Redis.

    Args:
        method: The method being decorated.

    Returns:
        The wrapped method.
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Logs inputs and outputs """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    """
    Caches data in Redis & provides retrieval methods.
    """

    def __init__(self):
        """
        Initializes Redis client and flushes the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Stores data in Redis with a random key.

        Args:
            data: Data to store (str, bytes, int, float).

        Returns:
            Randomly generated key used for storage.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data from Redis & optionally applies a conversion function.

        Args:
            key: Key to retrieve data from Redis.
            fn: Optional conversion function.

        Returns:
            Retrieved data, possibly converted based on fn.
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_int(self: bytes) -> int:
        """Converts bytes to int."""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """
        Retrieves UTF-8 string from Redis.

        Returns:
            Retrieved UTF-8 string.
        """
        return self.decode("utf-8")
