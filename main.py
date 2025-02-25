"""
main.py

Entry point for the Intelligent Lift Control System simulation in a multi-lift setup,
integrating a GUI (Approach 2). We:
  1. Parse an input file or use a default configuration.
  2. Prepare the lifts (from simulation.py) without a blocking loop.
  3. Pass the lifts into the GUI, which handles scheduling steps visually.
"""

import sys
from typing import Dict, Any
from simulation import prepare_lifts
from utils import log_event

import tkinter as tk
from gui import MultiLiftGUI

def parse_input_file(file_path: str) -> Dict[str, Any]:
    config: Dict[str, Any] = {}
    requests: Dict[int, list] = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                cleaned_lines.append(line)
        if not cleaned_lines:
            raise ValueError("Input file is empty or only comments.")
        first_line = cleaned_lines[0]
        parts = first_line.split(',')
        if len(parts) != 2:
            raise ValueError("First line must be 'num_floors, capacity'.")
        num_floors = int(parts[0].strip())
        capacity = int(parts[1].strip())
        config["num_floors"] = num_floors
        config["capacity"] = capacity
        for line in cleaned_lines[1:]:
            if ':' not in line:
                continue
            floor_part, dest_part = line.split(':', 1)
            floor = int(floor_part.strip())
            dest_part = dest_part.strip()
            if dest_part == "":
                requests[floor] = []
            else:
                dest_list = [d.strip() for d in dest_part.split(',')]
                destinations = []
                for d in dest_list:
                    dest_floor = int(d)
                    if dest_floor == floor:
                        raise ValueError(f"Request from floor {floor} to same floor {dest_floor} not allowed.")
                    destinations.append(dest_floor)
                requests[floor] = destinations
        config["requests"] = requests
        config["algorithm"] = "SCAN"
        config["simulation_time"] = 100
        return config
    except Exception as e:
        raise ValueError(f"Error parsing input file '{file_path}': {e}")

def main() -> None:
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        try:
            config = parse_input_file(input_file)
        except ValueError as ve:
            log_event(f"[ERROR] {ve}")
            sys.exit(1)
    else:
        config = {
            "num_floors": 5,
            "capacity": 4,
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
    if "num_lifts" not in config:
        config["num_lifts"] = 2
    log_event(f"Starting simulation with configuration: {config}")
    lifts = prepare_lifts(config)
    root = tk.Tk()
    gui = MultiLiftGUI(root, lifts=lifts, algorithm=config.get("algorithm", "SCAN"),
                       num_floors=config["num_floors"], num_lifts=config["num_lifts"])
    root.mainloop()
    log_event("GUI simulation completed.")

if __name__ == "__main__":
    main()