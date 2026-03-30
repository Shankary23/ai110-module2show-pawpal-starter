from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: str        # "low", "medium", "high"
    date: str            # format: "YYYY-MM-DD"
    frequency: str       # "once", "daily", "weekly"
    completed: bool = False

    def get_details(self) -> str:
        """Return a formatted summary string of the task."""
        status = "done" if self.completed else "pending"
        return f"{self.description} | {self.duration_minutes} min | {self.priority} priority | {self.frequency} | {self.date} | {status}"

    def get_priority(self) -> str:
        """Return the priority level of the task."""
        return self.priority

    def get_date(self) -> str:
        """Return the scheduled date of the task."""
        return self.date

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def get_name(self) -> str:
        """Return the pet's name."""
        return self.name

    def get_details(self) -> str:
        """Return a formatted summary string of the pet."""
        return f"Pet: {self.name} ({self.species}), Tasks: {len(self.tasks)}"

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks belonging to this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: List[Pet] = field(default_factory=list)

    def get_name(self) -> str:
        """Return the owner's name."""
        return self.name

    def get_details(self) -> str:
        """Return a formatted summary string of the owner and their pets."""
        pet_names = ", ".join(p.get_name() for p in self.pets) or "none"
        return f"Owner: {self.name}, Available: {self.available_minutes} min/day, Pets: {pet_names}"

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.get_tasks()]


class Scheduler:
    def __init__(self, owner: Owner, target_date: str):
        self.owner = owner
        self.target_date = target_date  # format: "YYYY-MM-DD"

    def get_pending_tasks(self) -> List[Task]:
        """Return all incomplete tasks across all pets for the target date."""
        return [t for t in self.owner.get_all_tasks()
                if t.date == self.target_date and not t.completed]

    def generate_schedule(self) -> List[Task]:
        """Return a prioritized list of tasks that fit within the owner's available time."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending = self.get_pending_tasks()
        sorted_tasks = sorted(pending, key=lambda t: priority_order[t.priority])

        plan, total = [], 0
        for task in sorted_tasks:
            if total + task.duration_minutes <= self.owner.available_minutes:
                plan.append(task)
                total += task.duration_minutes
        return plan

    def explain_plan(self) -> str:
        """Return a human-readable summary of the scheduled tasks and total time used."""
        plan = self.generate_schedule()
        if not plan:
            return "No tasks could be scheduled for this day."
        lines = [f"Schedule for {self.owner.get_name()}'s pets on {self.target_date}:"]
        total = 0
        for task in plan:
            total += task.duration_minutes
            lines.append(f"  - {task.description} ({task.duration_minutes} min, {task.priority} priority, {task.frequency})")
        lines.append(f"Total time: {total} min / {self.owner.available_minutes} min available")
        return "\n".join(lines)

    def mark_task_complete(self, description: str):
        """Find a task by description across all pets and mark it as complete."""
        for task in self.owner.get_all_tasks():
            if task.description == description:
                task.mark_complete()
                return
