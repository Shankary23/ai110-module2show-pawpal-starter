from pawpal_system import Owner, Pet, Task, Scheduler

TODAY = "2026-03-29"
TOMORROW = "2026-03-30"
NEXT_WEEK = "2026-04-05"


def make_task(description="Morning walk", duration=30, priority="high",
              frequency="daily", date=TODAY, time="07:00"):
    return Task(
        description=description,
        duration_minutes=duration,
        priority=priority,
        date=date,
        frequency=frequency,
        time=time
    )


def make_scheduler(available=90, tasks=None):
    """Helper: build an owner + pet + scheduler with optional task list."""
    owner = Owner(name="Jordan", available_minutes=available)
    pet = Pet(name="Mochi", species="dog")
    for t in (tasks or []):
        pet.add_task(t)
    owner.add_pet(pet)
    return Scheduler(owner=owner, target_date=TODAY)


# ---------------------------------------------------------------------------
# Task basics
# ---------------------------------------------------------------------------

def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_mark_complete_is_idempotent():
    """Marking an already-complete task complete should not raise."""
    task = make_task()
    task.mark_complete()
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(make_task("Morning walk"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(make_task("Evening walk"))
    assert len(pet.get_tasks()) == 2


# ---------------------------------------------------------------------------
# next_occurrence
# ---------------------------------------------------------------------------

def test_next_occurrence_daily():
    task = make_task(frequency="daily", date=TODAY)
    nxt = task.next_occurrence()
    assert nxt.date == TOMORROW
    assert nxt.completed == False


def test_next_occurrence_weekly():
    task = make_task(frequency="weekly", date=TODAY)
    nxt = task.next_occurrence()
    assert nxt.date == NEXT_WEEK
    assert nxt.completed == False


def test_next_occurrence_once_returns_none():
    task = make_task(frequency="once")
    assert task.next_occurrence() is None


def test_next_occurrence_preserves_attributes():
    task = make_task(description="Flea medicine", duration=5,
                     priority="high", frequency="weekly", time="08:00")
    nxt = task.next_occurrence()
    assert nxt.description == "Flea medicine"
    assert nxt.duration_minutes == 5
    assert nxt.priority == "high"
    assert nxt.time == "08:00"


# ---------------------------------------------------------------------------
# generate_schedule — priority and time budget
# ---------------------------------------------------------------------------

def test_high_priority_scheduled_before_low():
    tasks = [
        make_task("Low task",  duration=10, priority="low"),
        make_task("High task", duration=10, priority="high"),
    ]
    scheduler = make_scheduler(available=90, tasks=tasks)
    plan = scheduler.generate_schedule()
    assert plan[0].description == "High task"


def test_tasks_exceeding_budget_are_excluded():
    tasks = [
        make_task("Big task", duration=80, priority="high"),
        make_task("Huge task", duration=80, priority="high", time="09:00"),
    ]
    scheduler = make_scheduler(available=90, tasks=tasks)
    plan = scheduler.generate_schedule()
    assert len(plan) == 1
    assert plan[0].description == "Big task"


def test_empty_task_list_returns_empty_schedule():
    scheduler = make_scheduler(available=90, tasks=[])
    assert scheduler.generate_schedule() == []


def test_completed_tasks_excluded_from_schedule():
    task = make_task()
    task.mark_complete()
    scheduler = make_scheduler(tasks=[task])
    assert scheduler.generate_schedule() == []


def test_wrong_date_task_excluded_from_schedule():
    task = make_task(date="2025-01-01")
    scheduler = make_scheduler(tasks=[task])
    assert scheduler.generate_schedule() == []


def test_exactly_fitting_task_is_included():
    task = make_task(duration=90)
    scheduler = make_scheduler(available=90, tasks=[task])
    assert task in scheduler.generate_schedule()


# ---------------------------------------------------------------------------
# sort_by_time
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    tasks = [
        make_task("C", time="18:00"),
        make_task("A", time="07:00"),
        make_task("B", time="09:30"),
    ]
    scheduler = make_scheduler(tasks=tasks)
    sorted_tasks = scheduler.sort_by_time()
    assert [t.description for t in sorted_tasks] == ["A", "B", "C"]


def test_sort_by_time_excludes_completed():
    done = make_task("Done task", time="06:00")
    done.mark_complete()
    pending = make_task("Pending task", time="10:00")
    scheduler = make_scheduler(tasks=[done, pending])
    result = scheduler.sort_by_time()
    assert len(result) == 1
    assert result[0].description == "Pending task"


# ---------------------------------------------------------------------------
# filter_by_status
# ---------------------------------------------------------------------------

def test_filter_pending_returns_only_incomplete():
    done = make_task("Done")
    done.mark_complete()
    pending = make_task("Pending", time="09:00")
    scheduler = make_scheduler(tasks=[done, pending])
    result = scheduler.filter_by_status(completed=False)
    assert all(not t.completed for t in result)
    assert any(t.description == "Pending" for t in result)


def test_filter_completed_returns_only_done():
    done = make_task("Done")
    done.mark_complete()
    pending = make_task("Pending", time="09:00")
    scheduler = make_scheduler(tasks=[done, pending])
    result = scheduler.filter_by_status(completed=True)
    assert all(t.completed for t in result)


# ---------------------------------------------------------------------------
# filter_by_pet
# ---------------------------------------------------------------------------

def test_filter_by_pet_returns_correct_tasks():
    owner = Owner(name="Jordan", available_minutes=90)
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    mochi.add_task(make_task("Walk"))
    luna.add_task(make_task("Litter box", time="09:00"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    assert all(t.description == "Walk" for t in scheduler.filter_by_pet("Mochi"))
    assert all(t.description == "Litter box" for t in scheduler.filter_by_pet("Luna"))


def test_filter_by_pet_is_case_insensitive():
    owner = Owner(name="Jordan", available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(make_task())
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    assert len(scheduler.filter_by_pet("mochi")) == 1
    assert len(scheduler.filter_by_pet("MOCHI")) == 1


def test_filter_by_pet_unknown_name_returns_empty():
    scheduler = make_scheduler(tasks=[make_task()])
    assert scheduler.filter_by_pet("Ghost") == []


# ---------------------------------------------------------------------------
# detect_conflicts
# ---------------------------------------------------------------------------

def test_no_conflicts_when_times_differ():
    owner = Owner(name="Jordan", available_minutes=90)
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    mochi.add_task(make_task("Walk", time="07:00"))
    luna.add_task(make_task("Litter", time="09:00"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    assert scheduler.detect_conflicts() == []


def test_conflict_detected_when_times_match():
    owner = Owner(name="Jordan", available_minutes=90)
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    mochi.add_task(make_task("Walk",   time="07:00"))
    luna.add_task(make_task("Bath",    time="07:00"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "07:00" in conflicts[0]
    assert "WARNING" in conflicts[0]


def test_conflict_message_names_both_pets():
    owner = Owner(name="Jordan", available_minutes=90)
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    mochi.add_task(make_task("Walk", time="08:00"))
    luna.add_task(make_task("Bath", time="08:00"))
    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    conflicts = scheduler.detect_conflicts()
    assert "Mochi" in conflicts[0]
    assert "Luna" in conflicts[0]


# ---------------------------------------------------------------------------
# mark_task_complete + auto-rescheduling
# ---------------------------------------------------------------------------

def test_mark_task_complete_marks_done():
    task = make_task("Walk", frequency="once")
    scheduler = make_scheduler(tasks=[task])
    scheduler.mark_task_complete("Walk")
    assert task.completed == True


def test_daily_task_auto_schedules_next_day():
    task = make_task("Walk", frequency="daily")
    owner = Owner(name="Jordan", available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    scheduler.mark_task_complete("Walk")
    dates = [t.date for t in pet.get_tasks()]
    assert TOMORROW in dates


def test_once_task_does_not_reschedule():
    task = make_task("Vet visit", frequency="once")
    owner = Owner(name="Jordan", available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(task)
    owner.add_pet(pet)
    scheduler = Scheduler(owner=owner, target_date=TODAY)
    scheduler.mark_task_complete("Vet visit")
    assert len(pet.get_tasks()) == 1  # no new task added


def test_mark_nonexistent_task_does_not_raise():
    """Completing a task that doesn't exist should silently do nothing."""
    scheduler = make_scheduler(tasks=[make_task()])
    scheduler.mark_task_complete("This task does not exist")
