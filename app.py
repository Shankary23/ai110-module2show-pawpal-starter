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
st.subheader("Tasks")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_desc = st.text_input("Description", value="Morning walk")
with col2:
    duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

if st.button("Add task"):
    if st.session_state.current_pet is None:
        st.warning("Set an owner and pet first.")
    else:
        task = Task(
            description=task_desc,
            duration_minutes=int(duration),
            priority=priority,
            date=str(target_date),
            frequency=frequency
        )
        st.session_state.current_pet.add_task(task)
        st.session_state.tasks.append(task)
        st.success(f"Added '{task_desc}' to {st.session_state.current_pet.get_name()}.")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table([{
        "pet": next((p.get_name() for p in st.session_state.owner.pets if t in p.get_tasks()), ""),
        "description": t.description,
        "duration_minutes": t.duration_minutes,
        "priority": t.priority,
        "frequency": t.frequency,
        "completed": t.completed
    } for t in st.session_state.tasks])
else:
    st.info("No tasks yet. Add one above.")

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
        else:
            st.warning("No tasks fit within the available time, or no tasks match the selected date.")
