#!/usr/bin/env python3
"""
Implementation of a get_page function using requests and Redis for caching.
"""

import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """Decorator to cache and count URL accesses."""
    @wraps(method)
    def wrapper(url):
        """Wrapper function for caching and counting."""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """Fetches HTML content of a URL."""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
