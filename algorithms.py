"""
algorithms.py

Implements single-lift scheduling algorithms (SCAN_lift, LOOK_lift, MYLIFT_lift)
for a multi-lift scenario. Each function operates on a Lift instance.

We do not import 'calculatePriority' from utils anymore. 
Any priority logic is done inline in MYLIFT_lift.
"""

from typing import Dict
from lift import Lift

def SCAN_lift(lift: Lift, top_floor: int) -> None:
    """
    Implements a full SCAN scheduling algorithm for a single Lift object.
    Blocks until lift.requests is empty.
    """
    while lift.requests:
        up_requests = [r for r in lift.requests if r > lift.current_floor]
        down_requests = [r for r in lift.requests if r < lift.current_floor]

        if lift.direction == "UP":
            if up_requests:
                old_floor = lift.current_floor
                if lift.current_floor < top_floor:
                    lift.current_floor += 1
                    lift.floors_traveled += abs(lift.current_floor - old_floor)
            else:
                lift.direction = "DOWN"
                if down_requests:
                    old_floor = lift.current_floor
                    if lift.current_floor > 1:
                        lift.current_floor -= 1
                        lift.floors_traveled += abs(lift.current_floor - old_floor)

        elif lift.direction == "DOWN":
            if down_requests:
                old_floor = lift.current_floor
                if lift.current_floor > 1:
                    lift.current_floor -= 1
                    lift.floors_traveled += abs(lift.current_floor - old_floor)
            else:
                lift.direction = "UP"
                if up_requests:
                    old_floor = lift.current_floor
                    if lift.current_floor < top_floor:
                        lift.current_floor += 1
                        lift.floors_traveled += abs(lift.current_floor - old_floor)

        # If we arrived at a request floor, remove it
        if lift.current_floor in lift.requests:
            lift.requests.remove(lift.current_floor)
            lift.serviced_requests += 1


def LOOK_lift(lift: Lift) -> None:
    """
    Full LOOK scheduling for a single Lift object.
    Similar to SCAN but reverses direction immediately if 
    no requests exist in the current direction.
    """
    while lift.requests:
        up_requests = [r for r in lift.requests if r > lift.current_floor]
        down_requests = [r for r in lift.requests if r < lift.current_floor]

        if lift.direction == "UP":
            if up_requests:
                old_floor = lift.current_floor
                target_floor = min(up_requests)
                if lift.current_floor < target_floor:
                    lift.current_floor += 1
                    lift.floors_traveled += abs(lift.current_floor - old_floor)
            else:
                lift.direction = "DOWN"
                if down_requests:
                    old_floor = lift.current_floor
                    target_floor = max(down_requests)
                    if lift.current_floor > target_floor:
                        lift.current_floor -= 1
                        lift.floors_traveled += abs(lift.current_floor - old_floor)

        elif lift.direction == "DOWN":
            if down_requests:
                old_floor = lift.current_floor
                target_floor = max(down_requests)
                if lift.current_floor > target_floor:
                    lift.current_floor -= 1
                    lift.floors_traveled += abs(lift.current_floor - old_floor)
            else:
                lift.direction = "UP"
                if up_requests:
                    old_floor = lift.current_floor
                    target_floor = min(up_requests)
                    if lift.current_floor < target_floor:
                        lift.current_floor += 1
                        lift.floors_traveled += abs(lift.current_floor - old_floor)

        # Remove serviced request if we've landed on it
        if lift.current_floor in lift.requests:
            lift.requests.remove(lift.current_floor)
            lift.serviced_requests += 1


def MYLIFT_lift(lift: Lift, timeWaited: Dict[int, int]) -> None:
    """
    A custom MYLIFT algorithm for a single Lift instance.
    Does priority logic inline: priority = distance - wait_time
    (lower numeric value = higher priority).
    """
    while lift.requests:
        # Build a local list of floors
        pending = lift.requests[:]

        best_priority = float('inf')
        best_floor = None
        for floor_req in pending:
            wait_time = timeWaited.get(floor_req, 0)
            # inline priority calc: distance - wait_time
            priority = abs(floor_req - lift.current_floor) - wait_time
            if priority < best_priority:
                best_priority = priority
                best_floor = floor_req

        # Move 1 floor closer
        if best_floor is not None:
            old_floor = lift.current_floor
            if best_floor > lift.current_floor:
                lift.current_floor += 1
                lift.direction = "UP"
            elif best_floor < lift.current_floor:
                lift.current_floor -= 1
                lift.direction = "DOWN"
            lift.floors_traveled += abs(lift.current_floor - old_floor)

            # If arrived
            if lift.current_floor == best_floor:
                lift.requests.remove(best_floor)
                lift.serviced_requests += 1

        # Increment waiting times
        for floor_req in lift.requests:
            timeWaited[floor_req] = timeWaited.get(floor_req, 0) + 1