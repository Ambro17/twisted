from functools import lru_cache, wraps
from time import monotonic_ns


def lru_cache_with_ttl(
    ttl_in_seconds: int = 15 * 60, maxsize: int = 128, typed: bool = False
):
    """Extension over existing lru_cache that adds a timeout
    Usage:
        @lru_cache_with_ttl(ttl_in_seconds=15 * 60)
        def my_func():
            expensive_api_call()
    """

    def function_with_memory(f):
        """
        Line below would be equivalent to
        @lru_cache(maxsize, typed)
        def f():
            pass
        """
        f = lru_cache(maxsize=maxsize, typed=typed)(f)

        # Set expiration time to ttl_in_ns
        f.ttl_in_ns = ttl_in_seconds * 10 ** 9  
        f.expiration = monotonic_ns() + f.ttl_in_ns

        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if monotonic_ns() >= f.expiration:
                # Clear the cache and set next expiration time
                f.cache_clear()
                f.expiration = monotonic_ns() + f.ttl_in_ns

            return f(*args, **kwargs)

        wrapped_f.cache_info = f.cache_info
        wrapped_f.cache_clear = f.cache_clear
        return wrapped_f

    return function_with_memory
