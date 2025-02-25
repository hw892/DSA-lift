# Intelligent Lift Control System (GUI Edition)

**University of Exeter – February 2025**  
**Module: Data Structures and Algorithms**

---

## Overview

This project implements an **Intelligent Lift Control System** that handles multiple lifts and schedules their movements using classical and custom algorithms. The solution features a **Tkinter-based graphical user interface (GUI)**, allowing users to watch the lifts move floor-by-floor in real time. It aims to demonstrate fundamental data structures, scheduling algorithms (SCAN, LOOK, and MYLIFT), and practical GUI design for an academic module at the University of Exeter.

---

## Features

1. **Multi-Lift Scheduling**  
   - Supports multiple lifts in a multi-storey building.  
   - Distributes floor requests amongst lifts to minimise wait times.

2. **Algorithms**  
   - **SCAN**: Moves in one direction until the top/bottom floor is reached, then reverses.  
   - **LOOK**: Like SCAN but reverses direction earlier if no further requests exist.  
   - **MYLIFT**: A custom heuristic algorithm, combining waiting times and distance to floors.

3. **Tkinter GUI**  
   - Non-blocking simulation using `root.after()`, ensuring the interface remains responsive.  
   - Smooth, incremental animation for each lift’s movement, displayed floor-by-floor.  
   - Clear visual indicators of floors, lifts, and the current algorithm.

4. **Configuration and Extensibility**  
   - Reads from an input file (if provided) specifying the number of floors, capacity, and floor requests.  
   - Additional algorithms or data structures may be added with minimal refactoring.

---

## Installation and Requirements

**Important**: macOS system Python (with `_tkinter` deprecation) may cause a blank or unresponsive GUI window. For best results:

1. **Install** [Miniconda or Anaconda](https://www.anaconda.com/products/distribution)  

2. **Create** a dedicated environment with Python that supports Tkinter:
   ```bash
   conda create -n tk-env python
   conda activate tk-env

3.	Clone or download this repository into a local folder.

4.	(Optional) Install any additional dependencies (e.g., if pip install ... is required).

On Windows or Linux, the default Python distribution typically includes Tkinter. On macOS, the recommended approach is to use either a Conda environment or the official python.org installer.

## Usage
1.	Activate your Python environment (if using Conda):
conda activate tk-env

2.	Navigate to the project directory:
cd "/path/to/Data Structures and Algorithms Group Project"

3.	Run the main script:
python main.py
•	If you have an input file, e.g. input.txt, specify it:
python main.py input.txt

4.	GUI will appear with a “Start Simulation” button:
	
•	Click “Start Simulation” to watch the lifts move floor by floor.

•	Once completed, you will see the total requests serviced and floors travelled.

## Project Structure
Data Structures and Algorithms Group Project
├── main.py            # Entry point: parses input file, config, launches GUI
├── gui.py             # Tkinter GUI: Non-blocking simulation loop, animations
├── lift.py            # Defines the Lift class (one-floor-at-a-time movement)
├── simulation.py      # Prepares lifts from the config (distributes requests)
├── algorithms.py      # (Optional) If SCAN, LOOK, MYLIFT code is separate
├── utils.py           # Logging or shared helper functions
├── input_low.txt      # Example input file (low traffic)
├── input_high.txt     # Example input file (high traffic)
├── input_mixed.txt    # Example input file (mixed scenarios)
└── README.md          # This README

1.	main.py
	•	Reads configuration (number of floors, capacity, requests).
	•	Calls prepare_lifts(config) to distribute requests among lifts.
	•	Instantiates MultiLiftGUI and starts the Tkinter main loop.

2.	gui.py
	•	Provides a non-blocking loop (root.after()) for simulation steps.
	•	Animates lifts with smooth transitions, draws floor lines, handles user interactions.

3.	lift.py
	•	Lift class representing each elevator.
	•	Maintains current floor, direction, requests, floors travelled, etc.
	•	Typically moves one floor at a time via next_step().

4.	simulation.py
	•	Contains prepare_lifts(config) to create multiple Lift objects.
	•	Distributes requests among lifts in a simple or user-defined manner.

5.	algorithms.py (If used)
	•	Potentially hosts single-step versions of SCAN, LOOK, MYLIFT.
	•	May be called by the lifts or the GUI to move each lift floor by floor.

6.	utils.py
	•	Logging (log_event) or other utility methods.

## Algorithms
1.	SCAN
	•	Moves upward until reaching the highest requested floor or top floor, then reverses.
	•	Services all requests in the current direction before changing direction.

2.	LOOK
	•	Similar to SCAN but looks ahead: if no more requests exist in the current direction, it reverses earlier.

3.	MYLIFT
	•	A custom heuristic that factors in distance to floors and waiting times.
	•	A single-step approach ensures it only moves one floor per tick, suitable for GUI animation
    
## Example Scenarios
1.	Low Traffic (input_low.txt):
	•	Few requests, typically tests basic movement.

2.	High Traffic (input_high.txt):
	•	Many requests, ensures the lifts can handle numerous floors.

3.	Mixed (input_mixed.txt):
	•	Various requests in random patterns, testing overall performance.

## Known Issues or Limitations
•	MacOS System Python: The default system _tkinter is deprecated and may display a blank window. Use Conda or python.org Python.

•	Scalability: Although it can handle many floors, the GUI’s canvas might become cluttered with extremely large building sizes.

•	Algorithm Variation: Single-step versions of LOOK and MYLIFT must be carefully coded to integrate with the non-blocking GUI loop.

## Future Enhancements
•	Real-Time Request Insertion: Add a button or method to insert new requests mid-simulation.

•	Multiple Buildings: Extend to multiple independent building simulations.

•	Performance Metrics: Graph or log average wait times, total distance, throughput, etc., in real time.

•	GUI Polish: Possibly add a side panel with real-time stats, or a floor-by-floor queue display.

MIT License

Copyright (c) 2025 University of Exeter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included 
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.