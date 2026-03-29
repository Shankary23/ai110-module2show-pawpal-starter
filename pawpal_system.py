from dataclasses import dataclass
from typing import List


@dataclass
class Owner:
    name: str
    available_minutes: int

    def get_name(self) -> str:
        return self.name

    def get_details(self) -> str:
        return f"Owner: {self.name}, Available: {self.available_minutes} min/day"


@dataclass
class Pet:
    name: str
    species: str
    owner: Owner

    def get_name(self) -> str:
        return self.name

    def get_details(self) -> str:
        return f"Pet: {self.name} ({self.species}), Owner: {self.owner.get_name()}"

    def get_owner(self) -> Owner:
        return self.owner


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    date: str      # format: "YYYY-MM-DD"

    def get_details(self) -> str:
        return f"{self.title} | {self.duration_minutes} min | priority: {self.priority} | date: {self.date}"

    def get_priority(self) -> str:
        return self.priority

    def get_date(self) -> str:
        return self.date


class Scheduler:
    def __init__(self, pet: Pet, tasks: List[Task], target_date: str):
        self.pet = pet
        self.tasks = tasks
        self.target_date = target_date  # format: "YYYY-MM-DD"

    def generate_schedule(self) -> List[Task]:
        priority_order = {"high": 0, "medium": 1, "low": 2}
        available = self.pet.owner.available_minutes
        filtered = [t for t in self.tasks if t.date == self.target_date]
        sorted_tasks = sorted(filtered, key=lambda t: priority_order[t.priority])

        plan, total = [], 0
        for task in sorted_tasks:
            if total + task.duration_minutes <= available:
                plan.append(task)
                total += task.duration_minutes
        return plan

    def explain_plan(self) -> str:
        plan = self.generate_schedule()
        if not plan:
            return "No tasks could be scheduled for this day."
        lines = [f"Schedule for {self.pet.get_name()} on {self.target_date}:"]
        total = 0
        for task in plan:
            total += task.duration_minutes
            lines.append(f"  - {task.title} ({task.duration_minutes} min, {task.priority} priority)")
        lines.append(f"Total time: {total} min / {self.pet.owner.available_minutes} min available")
        return "\n".join(lines)
