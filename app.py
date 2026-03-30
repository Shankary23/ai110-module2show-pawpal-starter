import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.divider()

# --- Session State Init ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "current_pet" not in st.session_state:
    st.session_state.current_pet = None
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Owner & Pet Setup ---
st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=10, max_value=480, value=90)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
target_date = st.date_input("Schedule date", value=date.today())

if st.button("Set Owner & Pet"):
    owner = Owner(name=owner_name, available_minutes=available_minutes)
    pet = Pet(name=pet_name, species=species)
    owner.add_pet(pet)
    st.session_state.owner = owner
    st.session_state.current_pet = pet
    st.session_state.tasks = []
    st.success(f"Created owner {owner_name} with pet {pet_name}.")

if st.button("Add another pet"):
    if st.session_state.owner is None:
        st.warning("Set an owner first.")
    else:
        new_pet = Pet(name=pet_name, species=species)
        st.session_state.owner.add_pet(new_pet)
        st.session_state.current_pet = new_pet
        st.success(f"Added pet {pet_name} and switched to them.")

if st.session_state.owner:
    pet_names = [p.get_name() for p in st.session_state.owner.pets]
    selected = st.selectbox("Active pet (tasks go to this pet)", pet_names)
    st.session_state.current_pet = next(
        p for p in st.session_state.owner.pets if p.get_name() == selected
    )

st.divider()

# --- Add Tasks ---
st.subheader("Add a Task")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_desc = st.text_input("Description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
with col5:
    task_time = st.text_input("Time (HH:MM)", value="07:00")

if st.button("Add task"):
    if st.session_state.current_pet is None:
        st.warning("Set an owner and pet first.")
    else:
        existing = [t.description for t in st.session_state.current_pet.get_tasks()
                    if t.date == str(target_date)]
        if task_desc in existing:
            st.warning(f"'{task_desc}' is already scheduled for {st.session_state.current_pet.get_name()} on {target_date}.")
        else:
            task = Task(
                description=task_desc,
                duration_minutes=int(duration),
                priority=priority,
                date=str(target_date),
                frequency=frequency,
                time=task_time
            )
            st.session_state.current_pet.add_task(task)
            st.session_state.tasks.append(task)
            st.success(f"Added '{task_desc}' to {st.session_state.current_pet.get_name()}.")

st.divider()

# --- Task Views ---
if st.session_state.owner and st.session_state.tasks:

    def pet_for(task):
        return next(
            (p.get_name() for p in st.session_state.owner.pets if task in p.get_tasks()), ""
        )

    scheduler = Scheduler(owner=st.session_state.owner, target_date=str(target_date))

    # Tabs for each view
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "All Tasks", "Sorted by Time", "Filter by Status", "Filter by Pet", "Conflicts"
    ])

    with tab1:
        st.subheader("All Tasks")
        st.table([{
            "Pet":        pet_for(t),
            "Description": t.description,
            "Duration":   f"{t.duration_minutes} min",
            "Priority":   t.priority,
            "Time":       t.time,
            "Frequency":  t.frequency,
            "Status":     "Done" if t.completed else "Pending",
        } for t in st.session_state.tasks])

    with tab2:
        st.subheader("Tasks Sorted by Time")
        sorted_tasks = scheduler.sort_by_time()
        if sorted_tasks:
            st.table([{
                "Time":        t.time,
                "Pet":         pet_for(t),
                "Description": t.description,
                "Duration":    f"{t.duration_minutes} min",
                "Priority":    t.priority,
            } for t in sorted_tasks])
        else:
            st.info("No pending tasks for the selected date.")

    with tab3:
        st.subheader("Filter by Status")
        status_filter = st.radio("Show", ["Pending", "Completed"], horizontal=True)
        filtered = scheduler.filter_by_status(completed=(status_filter == "Completed"))
        if filtered:
            st.table([{
                "Pet":         pet_for(t),
                "Description": t.description,
                "Duration":    f"{t.duration_minutes} min",
                "Priority":    t.priority,
                "Frequency":   t.frequency,
                "Date":        t.date,
            } for t in filtered])
        else:
            st.info(f"No {status_filter.lower()} tasks found.")

    with tab4:
        st.subheader("Filter by Pet")
        pet_names = [p.get_name() for p in st.session_state.owner.pets]
        chosen_pet = st.selectbox("Select pet", pet_names, key="filter_pet_select")
        pet_tasks = scheduler.filter_by_pet(chosen_pet)
        if pet_tasks:
            st.table([{
                "Description": t.description,
                "Duration":    f"{t.duration_minutes} min",
                "Priority":    t.priority,
                "Time":        t.time,
                "Frequency":   t.frequency,
                "Status":      "Done" if t.completed else "Pending",
            } for t in pet_tasks])
        else:
            st.info(f"No tasks found for {chosen_pet}.")

    with tab5:
        st.subheader("Conflict Detection")
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            for msg in conflicts:
                st.warning(msg)
        else:
            st.success("No scheduling conflicts detected.")

else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Mark Task Complete ---
st.subheader("Mark Task Complete")

pending_tasks = [t for t in st.session_state.tasks if not t.completed]
if pending_tasks:
    task_to_complete = st.selectbox(
        "Select a task to mark complete",
        options=pending_tasks,
        format_func=lambda t: f"{t.description} — {pet_for(t) if st.session_state.owner else ''} ({t.time})"
        if st.session_state.owner else t.description
    )
    if st.button("Mark complete"):
        scheduler = Scheduler(owner=st.session_state.owner, target_date=str(target_date))
        scheduler.mark_task_complete(task_to_complete.description)
        if task_to_complete.frequency in ("daily", "weekly"):
            st.success(f"'{task_to_complete.description}' marked complete. Next occurrence auto-scheduled.")
        else:
            st.success(f"'{task_to_complete.description}' marked complete.")
        st.rerun()
else:
    st.info("No pending tasks to complete.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate schedule"):
    if st.session_state.owner is None:
        st.warning("Set an owner and pet first.")
    elif not st.session_state.tasks:
        st.warning("Add at least one task first.")
    else:
        scheduler = Scheduler(owner=st.session_state.owner, target_date=str(target_date))
        plan = scheduler.generate_schedule()
        if plan:
            st.success(scheduler.explain_plan())
            st.table([{
                "Description": t.description,
                "Time":        t.time,
                "Duration":    f"{t.duration_minutes} min",
                "Priority":    t.priority,
                "Frequency":   t.frequency,
            } for t in plan])
        else:
            st.warning("No tasks fit within the available time, or no tasks match the selected date.")
