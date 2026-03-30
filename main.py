from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = "2026-03-29"

# --- Create Owner ---
jordan = Owner(name="Jordan", available_minutes=90)

# --- Create Pets ---
mochi = Pet(name="Mochi", species="dog")
luna  = Pet(name="Luna",  species="cat")

# --- Add Tasks to Mochi ---
mochi.add_task(Task(
    description="Morning walk",
    duration_minutes=30,
    priority="high",
    date=TODAY,
    frequency="daily"
))
mochi.add_task(Task(
    description="Flea medicine",
    duration_minutes=5,
    priority="high",
    date=TODAY,
    frequency="weekly"
))

# --- Add Tasks to Luna ---
luna.add_task(Task(
    description="Clean litter box",
    duration_minutes=10,
    priority="medium",
    date=TODAY,
    frequency="daily"
))
luna.add_task(Task(
    description="Brush fur",
    duration_minutes=15,
    priority="low",
    date=TODAY,
    frequency="weekly"
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
print("\nTask details:")
for task in scheduler.generate_schedule():
    print(" ", task.get_details())
