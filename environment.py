"""Finite four-way intersection environment used by the Streamlit demo."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
import random

DIRECTIONS = ("N", "S", "E", "W")
PHASES = {0: "North / South", 1: "East / West"}

@dataclass
class Vehicle:
    vehicle_id: str
    direction: str
    wait_time: int = 0
    status: str = "queued"

class TrafficEnv:
    """A finite episode. Every configured vehicle will eventually clear."""
    def __init__(self, service_rate: int = 2, switch_penalty: int = 1):
        self.service_rate, self.switch_penalty = service_rate, switch_penalty
        self.reset({direction: 0 for direction in DIRECTIONS})

    def reset(self, vehicle_counts: Dict[str, int] | None = None):
        # Calling reset() without a configuration remains useful for the
        # existing Q-learning training script; the Streamlit app always
        # supplies fixed user-selected counts.
        if vehicle_counts is None:
            vehicle_counts = {direction: random.randint(0, 5) for direction in DIRECTIONS}
        self.queues = {direction: [Vehicle(f"{direction}-{n + 1}", direction) for n in range(max(0, int(vehicle_counts.get(direction, 0))))] for direction in DIRECTIONS}
        self.completed, self.last_moved, self.last_stopped = [], [], []
        self.step_number, self.last_action = 0, None
        return self.state

    @property
    def state(self): return tuple(len(self.queues[direction]) for direction in DIRECTIONS)
    @property
    def done(self): return sum(self.state) == 0

    def choose_action(self) -> int:
        ns = len(self.queues["N"]) + len(self.queues["S"])
        ew = len(self.queues["E"]) + len(self.queues["W"])
        return self.last_action if ns == ew and self.last_action is not None else (0 if ns >= ew else 1)

    def step(self, action: int):
        if action not in PHASES: raise ValueError("action must be 0 (NS) or 1 (EW)")
        if self.done: return self.state, 0.0, self.metrics()
        open_directions = ("N", "S") if action == 0 else ("E", "W")
        capacity = max(0, self.service_rate - (self.switch_penalty if self.last_action is not None and action != self.last_action else 0))
        self.last_moved, self.last_stopped = [], []
        for direction in DIRECTIONS:
            amount = capacity if direction in open_directions else 0
            departing, waiting = self.queues[direction][:amount], self.queues[direction][amount:]
            for vehicle in departing: vehicle.status = "passed"
            for vehicle in waiting: vehicle.status, vehicle.wait_time = "stopped", vehicle.wait_time + 1
            self.completed.extend(departing); self.queues[direction] = waiting
            self.last_moved.extend(departing); self.last_stopped.extend(waiting)
        self.step_number += 1; self.last_action = action
        reward = -(sum(self.state) + sum(v.wait_time for v in self.last_stopped))
        return self.state, float(reward), self.metrics(reward)

    def metrics(self, reward: float = 0.0):
        waits = [v.wait_time for queue in self.queues.values() for v in queue] + [v.wait_time for v in self.completed]
        return {"queued": sum(self.state), "passed": len(self.completed), "total": sum(self.state) + len(self.completed), "moved_this_tick": len(self.last_moved), "stopped_this_tick": len(self.last_stopped), "total_wait": sum(waits), "average_wait": round(sum(waits) / len(waits), 2) if waits else 0.0, "max_wait": max(waits, default=0), "reward": round(reward, 2)}
