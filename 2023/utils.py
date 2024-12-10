"""
Useful functions to help with puzzles
"""

from functools import wraps
import time


def profiler(func):
    """Allows for a timing decorator on a function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args,**kwargs)
        print(f'Time taken by function {func.__name__} is: {time.time() - start:0.4f} seconds')

        return result
    return wrapper
