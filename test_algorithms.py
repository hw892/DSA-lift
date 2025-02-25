"""
test_algorithms.py

Unit tests for the multi-lift scheduling algorithms:
  - SCAN_lift
  - LOOK_lift
  - MYLIFT_lift

Each function is tested on a single Lift instance (from lift.py).
We check that the lift ends up on the correct floor, and that 
all requests are serviced by the end of the algorithm.
"""

import unittest
from lift import Lift
from algorithms import SCAN_lift, LOOK_lift, MYLIFT_lift

class TestAlgorithms(unittest.TestCase):

    def test_SCAN_lift(self):
        """
        Test SCAN_lift with a single lift that has a small set of requests.
        We'll check final position, requests serviced, etc.
        """
        lift = Lift(lift_id=0, start_floor=1, top_floor=5)

        # Add requests: floors 3 and 5
        lift.add_request(3)
        lift.add_request(5)

        # Run SCAN_lift. This will block until all requests are served.
        SCAN_lift(lift, top_floor=5)

        self.assertEqual(len(lift.requests), 0, 
                         "All requests should be cleared after SCAN_lift.")
        self.assertEqual(lift.current_floor, 5, 
                         "Lift should end on the topmost requested floor.")
        self.assertGreater(lift.floors_traveled, 0, 
                           "Lift should have traveled some floors.")
        self.assertEqual(lift.serviced_requests, 2, 
                         "Should have serviced exactly 2 requests.")

    def test_LOOK_lift(self):
        """
        Test LOOK_lift with a single lift that has upward requests only,
        ensuring it ends on the highest requested floor (5).
        """
        lift = Lift(lift_id=0, start_floor=2, top_floor=5)
        # Only upward requests so the final floor should be 5.
        lift.add_request(4)
        lift.add_request(5)
        
        LOOK_lift(lift)

        self.assertEqual(len(lift.requests), 0, 
                         "All requests should be cleared after LOOK_lift.")
        self.assertEqual(lift.current_floor, 5, 
                         "Lift should end at the highest requested floor (5).")
        self.assertGreater(lift.floors_traveled, 0, 
                           "Lift should have traveled some floors.")
        self.assertEqual(lift.serviced_requests, 2, 
                         "Should have serviced exactly 2 requests.")

    def test_MY_LIFT_lift(self):
        """
        Test MYLIFT_lift with a single lift. We'll pass in some waiting times (optional).
        """
        lift = Lift(lift_id=0, start_floor=1, top_floor=5)
        # Add multiple requests
        lift.add_request(3)
        lift.add_request(5)
        lift.add_request(2)

        timeWaited = {
            3: 0,
            5: 0,
            2: 0
        }

        MYLIFT_lift(lift, timeWaited)

        self.assertEqual(len(lift.requests), 0, 
                         "All requests should be cleared after MYLIFT_lift.")
        self.assertTrue(lift.current_floor in [2,3,5], 
                        "Lift might end at final serviced floor; depends on logic.")
        self.assertGreater(lift.floors_traveled, 0, 
                           "Lift should have traveled floors.")
        self.assertEqual(lift.serviced_requests, 3, 
                         "Should have serviced exactly 3 requests.")

if __name__ == '__main__':
    unittest.main()