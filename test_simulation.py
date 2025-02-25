"""
test_simulation.py

Unit tests for the multi-lift simulation module (simulation.py).
We primarily test that run_simulation executes without errors, 
handles multiple lifts and requests, and logs the final messages.
"""

import unittest
import sys
import os
from unittest.mock import patch
from simulation import run_simulation
from utils import log_event

class TestSimulation(unittest.TestCase):
    def test_run_simulation_default(self):
        """
        Test run_simulation with a default config-like dictionary 
        that includes multiple lifts and some requests.
        We'll ensure it runs without errors and logs a completion message.
        """
        config = {
            "num_floors": 5,
            "num_lifts": 2,
            "requests": {
                1: [3, 5],
                2: [4],
                3: [],
                4: [1],
                5: []
            },
            "algorithm": "SCAN",
            "simulation_time": 100
        }

        # Capture logs to verify final completion messages
        with self.assertLogs(level='INFO') as log:
            run_simulation(config)
        
        logs_joined = "\n".join(log.output)
        self.assertIn("Simulation complete.", logs_joined)
        self.assertIn("Total simulation time:", logs_joined)
        self.assertIn("Total travel distance:", logs_joined)
        self.assertIn("Total serviced requests:", logs_joined)
        self.assertIn("Throughput:", logs_joined)

    def test_run_simulation_mixed_requests(self):
        """
        Test run_simulation with a small building but multiple lifts 
        and a mix of requests (some above, some below).
        """
        config = {
            "num_floors": 6,
            "num_lifts": 3,
            "requests": {
                1: [2, 5],
                2: [4],
                3: [6],
                4: [1],
                5: [2],
                6: []
            },
            "algorithm": "LOOK",
            "simulation_time": 50
        }

        with self.assertLogs(level='INFO') as log:
            run_simulation(config)

        logs_joined = "\n".join(log.output)
        self.assertIn("Simulation complete.", logs_joined)
        # Optionally check for lift distribution logs, if you log them:
        # e.g. "Created 3 lifts and assigned requests among them."

        # We can also look for performance metrics
        self.assertIn("Total simulation time:", logs_joined)
        self.assertIn("Total travel distance:", logs_joined)
        self.assertIn("Total serviced requests:", logs_joined)
        self.assertIn("Throughput:", logs_joined)

if __name__ == "__main__":
    unittest.main()