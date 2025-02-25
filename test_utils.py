"""
test_utils.py

Unit tests for helper functions in utils.py in a multi-lift context.
We no longer reference single-lift functions like moveLift or calculatePriority.
Instead, we test logging and global performance counters:
    - total_distance
    - serviced_requests
"""

import unittest
import time
from unittest.mock import patch
from utils import (
    log_event,
    reset_total_distance,
    get_total_distance,
    add_to_total_distance,
    reset_serviced_count,
    get_serviced_count,
    increment_serviced_requests
)

class TestUtils(unittest.TestCase):

    def test_log_event(self):
        """
        Test that log_event logs messages at INFO level.
        """
        with self.assertLogs(level='INFO') as log:
            log_event("Test logging message.")
        logs_joined = "\n".join(log.output)
        self.assertIn("Test logging message.", logs_joined, "Logged message should contain test string.")

    def test_total_distance_counters(self):
        """
        Test the global distance counters: reset, add, and get.
        """
        reset_total_distance()
        self.assertEqual(get_total_distance(), 0, "Distance should be zero after reset.")
        
        add_to_total_distance(5)
        self.assertEqual(get_total_distance(), 5, "Distance should be 5 after adding 5 floors.")
        
        add_to_total_distance(3)
        self.assertEqual(get_total_distance(), 8, "Distance should now be 8 after adding 3 more floors.")

        # Reset again
        reset_total_distance()
        self.assertEqual(get_total_distance(), 0, "Distance should return to zero after reset.")

    def test_serviced_requests_counters(self):
        """
        Test the global serviced requests counters: reset, increment, get.
        """
        reset_serviced_count()
        self.assertEqual(get_serviced_count(), 0, "Serviced requests should be 0 after reset.")

        increment_serviced_requests()
        self.assertEqual(get_serviced_count(), 1, "Serviced requests should be 1 after first increment.")

        increment_serviced_requests()
        increment_serviced_requests()
        self.assertEqual(get_serviced_count(), 3, "Serviced requests should be 3 after two more increments.")

        # Reset again
        reset_serviced_count()
        self.assertEqual(get_serviced_count(), 0, "Should be back to 0 after reset.")

if __name__ == '__main__':
    unittest.main()