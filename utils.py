"""
utils.py

Provides helper functions for logging, performance metrics, and other 
utilities in a multi-lift scenario.
"""

import logging
import time

# Setup basic logging if needed
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)

# Global counters (if you want a global measure)
_total_distance = 0
_serviced_requests = 0

def log_event(message: str) -> None:
    """
    Logs a message using Python's logging module at INFO level.
    """
    logging.info(message)

def reset_total_distance() -> None:
    """
    Resets the global distance counter to zero.
    """
    global _total_distance
    _total_distance = 0

def get_total_distance() -> int:
    """
    Returns the global distance traveled (floors).
    """
    return _total_distance

def add_to_total_distance(amount: int) -> None:
    """
    Adds the given amount to the global distance counter.
    """
    global _total_distance
    _total_distance += amount

def reset_serviced_count() -> None:
    """
    Resets the global serviced requests counter to zero.
    """
    global _serviced_requests
    _serviced_requests = 0

def get_serviced_count() -> int:
    """
    Returns the global number of serviced requests (across all lifts).
    """
    return _serviced_requests

def increment_serviced_requests() -> None:
    """
    Increment the global serviced requests counter by 1.
    """
    global _serviced_requests
    _serviced_requests += 1