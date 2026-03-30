# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The following features were added to `pawpal_system.py` to make the scheduler more useful for a real pet owner:

### Sort by Time
`Scheduler.sort_by_time()` returns pending tasks in chronological order using Python's `sorted()` with a `lambda` key on the `task.time` field (`"HH:MM"` format). Because times are zero-padded strings, lexicographic order matches chronological order — no conversion needed.

### Filter by Status
`Scheduler.filter_by_status(completed: bool)` lets the owner view either pending or completed tasks across all pets and all dates. Pass `True` for done tasks, `False` for what still needs attention.

### Filter by Pet
`Scheduler.filter_by_pet(pet_name: str)` returns every task belonging to a named pet, using case-insensitive matching. Useful for reviewing one pet's full care history at a glance.

### Conflict Detection
`Scheduler.detect_conflicts()` scans all tasks and warns when two tasks share the same date and time slot — whether they belong to the same pet or different pets. Uses a `defaultdict(list)` to group tasks by `(date, time)` key for efficient lookup. Always returns a list of warning strings and never raises an exception.

### Auto-Rescheduling
`Task.next_occurrence()` computes the next due date for recurring tasks using Python's `timedelta`:
- `"daily"` → current date + 1 day
- `"weekly"` → current date + 7 days
- `"once"` → returns `None` (not rescheduled)

`Scheduler.mark_task_complete()` calls this automatically when a task is marked done, appending the new instance to the correct pet's task list so recurring care never falls off the schedule.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
