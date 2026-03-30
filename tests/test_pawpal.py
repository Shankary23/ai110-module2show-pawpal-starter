from pawpal_system import Pet, Task

TODAY = "2026-03-29"


def make_task(description="Morning walk", duration=30, priority="high"):
    return Task(
        description=description,
        duration_minutes=duration,
        priority=priority,
        date=TODAY,
        frequency="daily"
    )


def test_mark_complete_changes_status():
    task = make_task()
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0
    pet.add_task(make_task("Morning walk"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(make_task("Evening walk"))
    assert len(pet.get_tasks()) == 2
