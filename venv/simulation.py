"""
simulation.py

This module now only prepares multiple lifts by:
  - Defining a Request class (optional).
  - Parsing the config (floors, requests, etc.).
  - Creating multiple Lift objects (from lift.py).
  - Distributing requests among them (each lift stores its own requests).

We do NOT run SCAN/LOOK/MYLIFT or step-based loops here. 
That logic is handled by the GUI or other code.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any

from lift import Lift
from utils import log_event

@dataclass
class Request:
    """
    Represents a request from an origin floor to a destination floor.
    You can keep or remove this if you like. It's optional:
      - Because you might only need 'destination' in your multi-lift approach.
      - Or you can keep origin/destination for advanced logic or logging.
    """
    origin: int
    destination: int
    direction: str = field(init=False)  # "UP" or "DOWN"
    waiting_time: int = 0  # could be updated if advanced logic
    priority: int = 0      # used by MYLIFT if needed

    def __post_init__(self) -> None:
        if self.destination > self.origin:
            self.direction = "UP"
        elif self.destination < self.origin:
            self.direction = "DOWN"
        else:
            raise ValueError(
                f"Invalid request: origin {self.origin} and destination "
                f"{self.destination} are the same."
            )

def prepare_lifts(config: Dict[str, Any]) -> List[Lift]:
    """
    Creates multiple Lift objects, distributes requests among them, 
    and returns the list of lifts. We do NOT run SCAN/LOOK/MYLIFT 
    or any step-based approach here. The GUI or other external code
    will handle the scheduling logic (step by step or otherwise).

    :param config: 
      - 'num_floors': total floors
      - 'num_lifts': how many Lift objects to create
      - 'requests': mapping of floor -> list of destinations
      - (optional) other config data

    :return: A list of Lift instances (with assigned requests).
    """
    num_floors = config.get("num_floors", 5)
    num_lifts = config.get("num_lifts", 1)
    requests_dict: Dict[int, List[int]] = config.get("requests", {})

    # 1) Create multiple Lift objects
    lifts = [Lift(lift_id=i, start_floor=1, top_floor=num_floors) 
             for i in range(num_lifts)]

    # 2) Distribute requests among lifts
    for origin_floor, destinations in requests_dict.items():
        for dest_floor in destinations:
            try:
                _ = Request(origin=origin_floor, destination=dest_floor)
            except ValueError as ve:
                log_event(f"[ERROR] {ve}")
                continue  # skip invalid request
            # pick a lift with the fewest requests
            chosen_lift = min(lifts, key=lambda lf: len(lf.requests))
            chosen_lift.add_request(dest_floor)

    log_event(f"Prepared {len(lifts)} lifts and assigned requests among them.")
    return lifts

# Optionally, if you still want a CLI fallback, define a function
# run_simulation_cli(config) that does a step-based approach or 
# calls SCAN_lift/LOOK_lift for each lift. But that's outside 
# the scope if your GUI will do the scheduling steps.

if __name__ == "__main__":
    # Example usage
    example_config = {
        "num_floors": 5,
        "num_lifts": 2,
        "requests": {
            1: [3, 5],
            2: [4],
            3: [],
            4: [1],
            5: []
        },
        "algorithm": "SCAN",   # We won't run scheduling here, just storing it
        "simulation_time": 100
    }
    lifts = prepare_lifts(example_config)
    for lf in lifts:
        print(f"Lift {lf.lift_id} -> requests: {lf.requests}")
    print("Lifts are prepared; scheduling/animation is done externally.")