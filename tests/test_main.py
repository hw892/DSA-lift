"""
test_main.py

Unit tests for the main.py module in a multi-lift context.
We primarily test that 'main()' can parse an input file (or use default config)
and invoke run_simulation without crashing.
"""

import unittest
import os
import sys
from unittest.mock import patch
from main import main
from utils import log_event

class TestMain(unittest.TestCase):

    def test_main_with_no_args(self):
        """
        Test that calling main() with no command-line args 
        uses the default configuration and runs the simulation.
        We'll just ensure it doesn't crash.
        """
        # We'll patch sys.argv to simulate no arguments
        test_args = ["main.py"]  # no extra file
        with patch.object(sys, "argv", test_args):
            # Optionally capture log output with assertLogs
            with self.assertLogs(level='INFO') as log:
                main()
            # Check if logs contain certain phrases
            logs_joined = "\n".join(log.output)
            self.assertIn("Starting simulation with configuration", logs_joined)
            self.assertIn("Simulation completed.", logs_joined)

    def test_main_with_input_file(self):
        """
        Test that calling main() with a sample input file runs the simulation. 
        We won't parse real content, but we'll patch parse_input_file 
        or supply a mock file to confirm main() processes it.
        """
        # We'll create a temporary input file for demonstration.
        sample_input = """# Number of Floors, Capacity
5, 4
# Floor Requests
1: 3
2: 4
"""
        temp_filename = "temp_test_input.txt"
        with open(temp_filename, "w") as f:
            f.write(sample_input)

        test_args = ["main.py", temp_filename]
        try:
            with patch.object(sys, "argv", test_args):
                with self.assertLogs(level='INFO') as log:
                    main()
                logs_joined = "\n".join(log.output)
                self.assertIn(f"Starting simulation with configuration:", logs_joined)
                self.assertIn("Simulation completed.", logs_joined)
        finally:
            # Clean up temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

if __name__ == '__main__':
    unittest.main()