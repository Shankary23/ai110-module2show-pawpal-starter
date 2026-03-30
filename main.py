from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = "2026-03-29"

# --- Create Owner ---
jordan = Owner(name="Jordan", available_minutes=90)

# --- Create Pets ---
mochi = Pet(name="Mochi", species="dog")
luna  = Pet(name="Luna",  species="cat")

# --- Add Tasks OUT OF ORDER (intentionally scrambled times) ---
mochi.add_task(Task(
    description="Evening walk",
    duration_minutes=30,
    priority="high",
    date=TODAY,
    frequency="daily",
    time="18:30"
))
luna.add_task(Task(
    description="Brush fur",
    duration_minutes=15,
    priority="low",
    date=TODAY,
    frequency="weekly",
    time="14:00"
))
mochi.add_task(Task(
    description="Morning walk",
    duration_minutes=30,
    priority="high",
    date=TODAY,
    frequency="daily",
    time="07:00"
))
luna.add_task(Task(
    description="Clean litter box",
    duration_minutes=10,
    priority="medium",
    date=TODAY,
    frequency="daily",
    time="09:30"
))
mochi.add_task(Task(
    description="Flea medicine",
    duration_minutes=5,
    priority="high",
    date=TODAY,
    frequency="weekly",
    time="08:00"
))

# --- Register Pets with Owner ---
jordan.add_pet(mochi)
jordan.add_pet(luna)

# --- Run Scheduler ---
scheduler = Scheduler(owner=jordan, target_date=TODAY)

print("=" * 45)
print("         PAWPAL+ TODAY'S SCHEDULE")
print("=" * 45)
print(scheduler.explain_plan())
print("=" * 45)

# 1. Sorted by priority (existing behavior)
print("\n--- Sorted by Priority ---")
for task in scheduler.generate_schedule():
    print(f"  [{task.priority}] {task.description} ({task.duration_minutes} min)")

# 2. Sorted by time (new method) — should show chronological order
print("\n--- Sorted by Time ---")
for task in scheduler.sort_by_time():
    print(f"  {task.time} - {task.description}")

# 3. Filter: pending only
print("\n--- Pending Tasks ---")
for task in scheduler.filter_by_status(completed=False):
    print(f"  {task.description} | {task.get_priority()} priority")

# 4. Filter: completed only
print("\n--- Completed Tasks ---")
completed = scheduler.filter_by_status(completed=True)
if completed:
    for task in completed:
        print(f"  {task.description} | done")
else:
    print("  None")

# 5. Filter by pet name
print("\n--- Mochi's Tasks ---")
for task in scheduler.filter_by_pet("Mochi"):
    print(f"  {task.time} - {task.description} | {task.get_priority()} priority")

print("\n--- Luna's Tasks ---")
for task in scheduler.filter_by_pet("Luna"):
    print(f"  {task.time} - {task.description} | {task.get_priority()} priority")

# --- Test auto-rescheduling ---
print("\n" + "=" * 45)
print("   MARKING TASKS COMPLETE & AUTO-RESCHEDULING")
print("=" * 45)

scheduler.mark_task_complete("Morning walk")     # daily -> next: 2026-03-30
scheduler.mark_task_complete("Flea medicine")    # weekly -> next: 2026-04-05

print("\nMochi's tasks after completion (includes next occurrences):")
for task in scheduler.filter_by_pet("Mochi"):
    status = "done" if task.completed else "pending"
    print(f"  {task.date} {task.time} - {task.description} | {task.frequency} | {status}")

# --- Test conflict detection ---
print("\n" + "=" * 45)
print("         CONFLICT DETECTION")
print("=" * 45)

# Add two tasks at the exact same time to trigger a conflict
mochi.add_task(Task(
    description="Vet appointment",
    duration_minutes=60,
    priority="high",
    date=TODAY,
    frequency="once",
    time="09:30"   # same as Luna's "Clean litter box"
))
luna.add_task(Task(
    description="Bath time",
    duration_minutes=20,
    priority="medium",
    date=TODAY,
    frequency="once",
    time="07:00"   # same as Mochi's "Morning walk"
))

conflicts = scheduler.detect_conflicts()
if conflicts:
    print("\nConflicts found:")
    for c in conflicts:
        print(f"  ⚠  {c}")
else:
    print("\nNo conflicts found.")
