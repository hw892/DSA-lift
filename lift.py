"""
lift.py

This module defines a Lift class for a multi-lift approach.
Each Lift object manages its own queue of requested floors and
executes a simplified SCAN-like scheduling approach in next_step().
"""

class Lift:
    def __init__(self, lift_id: int, start_floor: int = 1, top_floor: int = 5):
        """
        :param lift_id: An identifier (e.g., 0, 1, 2) for this lift.
        :param start_floor: The floor this lift starts on.
        :param top_floor: The highest floor in the building (for SCAN boundaries).
        """
        self.lift_id = lift_id
        self.current_floor = start_floor
        self.top_floor = top_floor   # used by SCAN-like logic
        self.direction = "UP"       # either "UP" or "DOWN"
        
        # We store requests as a list of floors the lift needs to visit
        self.requests = []

        # Optional fields for performance tracking
        self.floors_traveled = 0
        self.serviced_requests = 0

    def add_request(self, dest_floor: int):
        """
        Add a new destination request to this lift's list of requested floors.
        """
        if dest_floor not in self.requests:
            self.requests.append(dest_floor)

    def next_step(self):
        """
        Advance one "step" in a SCAN-like scheduling approach:
          1) If we have no requests, do nothing.
          2) Otherwise, find requests in the current direction if possible.
          3) Move one floor closer to the next target.
          4) If no requests exist in the current direction, reverse direction (classic SCAN).

        Moves the lift exactly 1 floor at a time.
        """

        # Debug print to see what's happening each step
        print(f"[DEBUG] Lift {self.lift_id} next_step() called. "
              f"current_floor={self.current_floor}, direction={self.direction}, requests={self.requests}")

        if not self.requests:
            print(f"[DEBUG] Lift {self.lift_id}: No requests, returning.")
            return  # No requests to process

        # Separate requests above and below current_floor
        up_requests = [r for r in self.requests if r > self.current_floor]
        down_requests = [r for r in self.requests if r < self.current_floor]

        if self.direction == "UP":
            if up_requests:
                # Move up 1 floor
                self._move_up()
            else:
                # No up requests, reverse direction (SCAN)
                self.direction = "DOWN"
                if down_requests:
                    self._move_down()
                # else no requests in either direction => might be exactly on a request
        elif self.direction == "DOWN":
            if down_requests:
                self._move_down()
            else:
                # No down requests, reverse direction
                self.direction = "UP"
                if up_requests:
                    self._move_up()

        # Check if we've arrived at any request
        if self.current_floor in self.requests:
            print(f"[DEBUG] Lift {self.lift_id} arrived at requested floor {self.current_floor}. Servicing it.")
            self.requests.remove(self.current_floor)
            self.serviced_requests += 1

    def _move_up(self):
        """
        Move the lift 1 floor up, increment floors_traveled.
        """
        old_floor = self.current_floor
        if self.current_floor < self.top_floor:
            self.current_floor += 1
            traveled = abs(self.current_floor - old_floor)
            self.floors_traveled += traveled
            print(f"[DEBUG] Lift {self.lift_id} moved UP from {old_floor} to {self.current_floor}. "
                  f"floors_traveled={self.floors_traveled}")
        else:
            print(f"[DEBUG] Lift {self.lift_id} at top floor {self.top_floor}, can't move up.")

    def _move_down(self):
        """
        Move the lift 1 floor down, increment floors_traveled.
        """
        old_floor = self.current_floor
        if self.current_floor > 1:
            self.current_floor -= 1
            traveled = abs(self.current_floor - old_floor)
            self.floors_traveled += traveled
            print(f"[DEBUG] Lift {self.lift_id} moved DOWN from {old_floor} to {self.current_floor}. "
                  f"floors_traveled={self.floors_traveled}")
        else:
            print(f"[DEBUG] Lift {self.lift_id} at floor 1, can't move down further.")

    def __repr__(self):
        return (f"<Lift id={self.lift_id}, floor={self.current_floor}, "
                f"dir={self.direction}, requests={self.requests}>")