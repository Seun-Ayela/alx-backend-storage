# #!/usr/bin/env python3
# '''A module with tools for request caching and tracking.
# '''
# import redis
# import requests
# from functools import wraps
# from typing import Callable


# redis_store = redis.Redis()
# '''The module-level Redis instance.
# '''


# def data_cacher(method: Callable) -> Callable:
#     '''Caches the output of fetched data.
#     '''
#     @wraps(method)
#     def invoker(url) -> str:
#         '''The wrapper function for caching the output.
#         '''
#         redis_store.incr(f'count:{url}')
#         result = redis_store.get(f'result:{url}')
#         if result:
#             return result.decode('utf-8')
#         result = method(url)
#         redis_store.set(f'count:{url}', 0)
#         redis_store.setex(f'result:{url}', 10, result)
#         return result
#     return invoker


# @data_cacher
# def get_page(url: str) -> str:
#     '''Returns the content of a URL after caching the request's response,
#     and tracking the request.
#     '''
#     return requests.get(url).text


#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.

Start in a new file named web.py and do not reuse the code
written in exercise.py.

Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.
"""

import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_count(method):
    """decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cached_value = r.get(key)
        if cached_value:
            return cached_value.decode("utf-8")

            # Get new content and update cache
        key_count = "count:" + url
        html_content = method(url)

        r.incr(key_count)
        r.set(key, html_content, ex=10)
        r.expire(key, 10)
        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')