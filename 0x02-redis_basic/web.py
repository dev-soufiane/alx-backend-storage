#!/usr/bin/env python3
"""
Implementation of an expiring web cache and tracker.
"""

import redis
import requests
from typing import Callable
from functools import wraps

redis_client = redis.Redis()


def wrap_requests(fn: Callable) -> Callable:
    """Decorator that adds caching to the wrapped function.

    Args:
        fn: The function to be wrapped.

    Returns:
        The wrapped function.
    """

    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper function with caching logic.

        Args:
            url: The URL to fetch page content from.

        Returns:
            The HTML content of the page.
        """
        redis_client.incr(f"count:{url}")
        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        result = fn(url)
        redis_client.setex(f"cached:{url}", 10, result)
        return result
    return wrapper


@wrap_requests
def get_page(url: str) -> str:
    """Fetches the HTML content of a web page.

    Args:
        url: The URL of the web page.

    Returns:
        The HTML content of the web page.
    """
    response = requests.get(url)
    return response.text
