from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass
class Task:
    description: str
    duration_minutes: int
    priority: str        # "low", "medium", "high"
    date: str            # format: "YYYY-MM-DD"
    frequency: str       # "once", "daily", "weekly"
    time: str = "00:00"  # format: "HH:MM"
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

    def next_occurrence(self) -> "Task":
        """Return a new pending Task scheduled for the next daily or weekly occurrence.

        Computes the next due date using Python's timedelta:
          - "daily"  -> current date + 1 day
          - "weekly" -> current date + 7 days
          - "once"   -> returns None (non-recurring tasks are not rescheduled)

        The returned Task is a fresh copy with completed=False, preserving all
        other attributes (description, duration, priority, time) from the original.
        """
        current = date.fromisoformat(self.date)
        if self.frequency == "daily":
            next_date = current + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = current + timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            date=next_date.isoformat(),
            frequency=self.frequency,
            time=self.time,
        )


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

    def filter_by_status(self, completed: bool) -> List[Task]:
        """Return all tasks across every pet filtered by completion status.

        Args:
            completed: Pass True to retrieve finished tasks, False for pending ones.

        Searches across all pets and all dates — not limited to the target date.
        Useful for reviewing what has been done vs. what still needs attention.
        """
        return [t for t in self.owner.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return all tasks belonging to a specific pet, matched by name.

        Matching is case-insensitive ("mochi" == "Mochi").
        Returns an empty list if no pet with that name is found.
        Includes tasks across all dates and completion statuses.
        """
        for pet in self.owner.pets:
            if pet.name.lower() == pet_name.lower():
                return pet.get_tasks()
        return []

    def sort_by_time(self) -> List[Task]:
        """Return all pending tasks for the target date sorted chronologically.

        Uses sorted() with a lambda key on task.time ("HH:MM" string).
        Zero-padded "HH:MM" format sorts correctly as plain strings —
        lexicographic order matches chronological order without any conversion.
        Only includes incomplete tasks matching the target date.
        """
        pending = self.get_pending_tasks()
        return sorted(pending, key=lambda task: task.time)

    def detect_conflicts(self) -> List[str]:
        """Scan all pet tasks and return warning messages for scheduling conflicts.

        A conflict occurs when two or more tasks (across any pets) share the same
        date and time string. Uses a defaultdict to group tasks by (date, time) key,
        then reports any slot with more than one entry.

        Always returns a list — never raises an exception. If an unexpected error
        occurs internally, a single warning string is returned describing the failure.
        Returns an empty list if no conflicts are found.
        """
        try:
            time_slots = defaultdict(list)
            for pet in self.owner.pets:
                for task in pet.get_tasks():
                    if not task.date or not task.time:
                        continue  # skip tasks with missing date/time
                    time_slots[(task.date, task.time)].append((pet.name, task.description))

            conflicts = []
            for (date, time), entries in time_slots.items():
                if len(entries) > 1:
                    labels = ", ".join(f"{pet}: {desc}" for pet, desc in entries)
                    conflicts.append(f"WARNING: Conflict at {date} {time} -> {labels}")
            return conflicts
        except Exception as e:
            return [f"WARNING: Conflict detection failed unexpectedly: {e}"]

    def mark_task_complete(self, description: str):
        """Mark a task complete and auto-schedule the next occurrence for recurring tasks."""
        for pet in self.owner.pets:
            for task in pet.get_tasks():
                if task.description == description and not task.completed:
                    task.mark_complete()
                    next_task = task.next_occurrence()
                    if next_task:
                        pet.add_task(next_task)
                    return
