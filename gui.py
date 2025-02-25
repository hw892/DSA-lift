"""
gui.py

A Tkinter GUI for multiple lifts in a multi-lift scenario.
- Uses root.after() for a non-blocking simulation loop.
- Animates each lift's rectangle in small increments.
- Integrates single-step scheduling logic so each lift moves one floor at a time.
"""

import tkinter as tk
from algorithms import SCAN_lift, LOOK_lift, MYLIFT_lift  # Single-step algorithms if needed
from utils import log_event

class MultiLiftGUI:
    def __init__(self, root, lifts, algorithm="SCAN", num_floors=5, num_lifts=2):
        self.root = root
        self.root.title("Multi-Lift Simulation")
        self.root.geometry("800x600")
        self.root.configure(bg="white")

        self.lifts = lifts
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.algorithm = algorithm
        self.timeWaited = {}

        self.sim_running = False

        # Sizing parameters
        self.floor_height = 100
        self.lift_width = 50
        self.lift_height = 50
        self.canvas_height = self.num_floors * self.floor_height
        self.canvas_width = self.num_lifts * (self.lift_width + 80)

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Draw floors and labels
        for f in range(self.num_floors):
            y = self.canvas_height - f * self.floor_height
            self.canvas.create_line(0, y, self.canvas_width, y, fill="red", width=2)
            self.canvas.create_text(20, y - 15, text=f"Floor {f+1}", fill="black", font=('Arial', 10))

        # Draw lift rectangles and labels
        self.lift_rects = []
        for i, lift_obj in enumerate(self.lifts):
            x_offset = 40 + i * (self.lift_width + 80)
            start_y = self.canvas_height - (lift_obj.current_floor * self.floor_height) + 10
            rect = self.canvas.create_rectangle(
                x_offset, start_y,
                x_offset + self.lift_width, start_y + self.lift_height,
                fill="yellow", outline="blue", width=3
            )
            self.lift_rects.append(rect)
            self.canvas.create_text(x_offset + self.lift_width // 2, start_y - 10,
                                    text=f"Lift {i+1}", fill="blue", font=('Arial', 10, 'bold'))

        # Control frame with button and status label
        self.control_frame = tk.Frame(self.root, bg="white")
        self.control_frame.pack(fill=tk.X, pady=10)

        self.sim_button = tk.Button(self.control_frame, text="Start Simulation",
                                    command=self.run_simulation, bg="green", fg="white", font=('Arial', 12))
        self.sim_button.pack(side=tk.LEFT, padx=10)

        self.status_label = tk.Label(self.control_frame, text="Simulation ready",
                                     bg="white", font=('Arial', 12))
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.algo_label = tk.Label(self.control_frame, text=f"Algorithm: {self.algorithm}",
                                   bg="white", font=('Arial', 12, 'bold'))
        self.algo_label.pack(side=tk.RIGHT, padx=10)

    def run_simulation(self):
        if self.sim_running:
            return
        self.sim_running = True
        self.sim_button.config(text="Simulation Running...", state=tk.DISABLED)
        self.status_label.config(text="Simulation in progress")
        log_event("[INFO] Starting simulation loop (non-blocking).")
        for i, lf in enumerate(self.lifts):
            log_event(f"[INFO] Lift {i} initial: floor={lf.current_floor}, requests={lf.requests}")
        self.simulation_step()

    def simulation_step(self):
        if any(lift.requests for lift in self.lifts):
            log_event("[DEBUG] Simulation step: processing lifts...")
            for i, lift_obj in enumerate(self.lifts):
                if lift_obj.requests:
                    old_floor = lift_obj.current_floor
                    if self.algorithm.upper() == "SCAN":
                        lift_obj.next_step()  # Use SCAN single-step from your Lift class
                    elif self.algorithm.upper() == "LOOK":
                        self._look_single_step(lift_obj)
                    elif self.algorithm.upper() == "MYLIFT":
                        self._mylift_single_step(lift_obj)
                    if lift_obj.current_floor != old_floor:
                        log_event(f"[INFO] Lift {i} moved from {old_floor} to {lift_obj.current_floor}")
                        self.update_lift_position(i, lift_obj.current_floor)
                        self.status_label.config(text=f"Lift {i+1} -> Floor {lift_obj.current_floor}")
                else:
                    log_event(f"[DEBUG] Lift {i} has no requests left.")
            self.root.after(1000, self.simulation_step)
        else:
            log_event("[INFO] All lifts done servicing requests.")
            self.sim_button.config(text="Simulation Completed", state=tk.DISABLED)
            self.status_label.config(text="All requests processed")
            self.sim_running = False
            total_floors = sum(l.floors_traveled for l in self.lifts)
            total_req = sum(l.serviced_requests for l in self.lifts)
            stats = f"Results: {total_req} requests serviced, {total_floors} floors traveled"
            tk.Label(self.root, text=stats, bg="white", font=('Arial', 12, 'bold')).pack(pady=10)

    def _look_single_step(self, lift):
        if not lift.requests:
            return
        up_requests = [r for r in lift.requests if r > lift.current_floor]
        down_requests = [r for r in lift.requests if r < lift.current_floor]
        old_floor = lift.current_floor
        if lift.direction == "UP":
            if up_requests:
                target_floor = min(up_requests)
                if lift.current_floor < target_floor:
                    lift.current_floor += 1
                    lift.floors_traveled += abs(lift.current_floor - old_floor)
            else:
                lift.direction = "DOWN"
                if down_requests:
                    target_floor = max(down_requests)
                    if lift.current_floor > target_floor:
                        lift.current_floor -= 1
                        lift.floors_traveled += abs(lift.current_floor - old_floor)
        elif lift.direction == "DOWN":
            if down_requests:
                target_floor = max(down_requests)
                if lift.current_floor > target_floor:
                    lift.current_floor -= 1
                    lift.floors_traveled += abs(lift.current_floor - old_floor)
            else:
                lift.direction = "UP"
                if up_requests:
                    target_floor = min(up_requests)
                    if lift.current_floor < target_floor:
                        lift.current_floor += 1
                        lift.floors_traveled += abs(lift.current_floor - old_floor)
        if lift.current_floor in lift.requests:
            lift.requests.remove(lift.current_floor)
            lift.serviced_requests += 1

    def _mylift_single_step(self, lift):
        if not lift.requests:
            return
        pending = lift.requests[:]
        best_priority = float('inf')
        best_floor = None
        for floor_req in pending:
            wait_time = self.timeWaited.get(floor_req, 0)
            priority = abs(floor_req - lift.current_floor) - wait_time
            if priority < best_priority:
                best_priority = priority
                best_floor = floor_req
        old_floor = lift.current_floor
        if best_floor is not None:
            if best_floor > lift.current_floor:
                lift.current_floor += 1
                lift.direction = "UP"
            elif best_floor < lift.current_floor:
                lift.current_floor -= 1
                lift.direction = "DOWN"
            lift.floors_traveled += abs(lift.current_floor - old_floor)
            if lift.current_floor == best_floor:
                lift.requests.remove(best_floor)
                lift.serviced_requests += 1
        for fr in lift.requests:
            self.timeWaited[fr] = self.timeWaited.get(fr, 0) + 1

    def update_lift_position(self, lift_index: int, new_floor: int):
        rect_id = self.lift_rects[lift_index]
        x1, y1, x2, y2 = self.canvas.coords(rect_id)
        target_y = self.canvas_height - (new_floor * self.floor_height) + 10
        log_event(f"[DEBUG] Updating lift {lift_index} to floor {new_floor} (target_y={target_y})")
        def smooth_move():
            x1_, y1_, x2_, y2_ = self.canvas.coords(rect_id)
            if abs(y1_ - target_y) > 1:
                step = -1 if target_y < y1_ else 1
                self.canvas.move(rect_id, 0, step)
                self.root.after(20, smooth_move)
            else:
                self.canvas.coords(rect_id, x1_, target_y, x2_, target_y + self.lift_height)
                log_event(f"[DEBUG] Lift {lift_index} final rect coords: {self.canvas.coords(rect_id)}")
        smooth_move()

def main():
    from lift import Lift
    root = tk.Tk()
    # For local testing: create two lifts and hardcode some requests
    lifts = [
        Lift(lift_id=0, start_floor=1, top_floor=5),
        Lift(lift_id=1, start_floor=1, top_floor=5)
    ]
    lifts[0].requests = [3, 5]
    lifts[1].requests = [4, 5]
    gui = MultiLiftGUI(root, lifts=lifts, algorithm="SCAN", num_floors=5, num_lifts=len(lifts))
    root.mainloop()

if __name__ == "__main__":
    main()