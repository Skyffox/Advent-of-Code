# pylint: disable=line-too-long
"""
Useful functions to help with puzzles
"""

from functools import wraps
import time


def profiler(func):
    """
    A decorator to measure and log the execution time of a function.
    
    This decorator wraps the provided function and tracks the time it takes 
    to execute. The measured execution time is printed to the console 
    with a timestamp.

    Args:
        func (function): The function whose execution time needs to be measured.

    Returns:
        function: A wrapped version of the input function, which logs the execution time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time() # Record the start time of the function call
        result = func(*args, **kwargs) # Execute the original function
        elapsed_time = time.time() - start_time # Compute the elapsed time
        print(f"Execution time of '{func.__name__}': {elapsed_time:.4f} seconds")
        return result

    return wrapper
