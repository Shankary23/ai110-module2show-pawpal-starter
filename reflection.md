# PawPal+ Project Reflection

## 1. System Design
**Core Actions**
- Enter pet information and owner information
- Modify and add tasks
- Let users generate a schedule from those tasks



**a. Initial design**

- Briefly describe your initial UML design.
    - For the  intial UML design it was simpler with having classes to cover different user inputs and potential actions.

- What classes did you include, and what responsibilities did you assign to each?
    - The classes I included was a owner class that holds the owners data, a pet class that holds the pets information. A task class that stores different information about the task, like detail and date. Also a scheduler class that ties the pets, task and owner classes together.


**b. Design changes**

- Did your design change during implementation?
    - Yes I changed the design during the implmenation to add some more relations.

- If yes, describe at least one change and why you made it.
    - First linked the relation of owners to pets but also pets to owners. Next also tasks class linked tasks to a specific pet instead of owners only.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - It considers time, the day, completion and priority. 
- How did you decide which constraints mattered most?
    - Time is the most important since we need to find a corresponding slot, and then priority because of the way the priority works we need to make sure that its the next thing that is considered.
**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - One large tradeoff the scheduler makes is not being optimized. Its greedy so it will take the first task not the most optimal task.
- Why is that tradeoff reasonable for this scenario?
    - Its reasonable because it maintains the time priority and makes sure that the highest priority tasks are always scheduled.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?



---

## 4. Testing and Verification

**Core Behaviors** 
- Prioirty based scheduling
- Task completion and recurring tasks to create future occuerences
- Conflict detection

**a. What you tested**

- What behaviors did you test?
    - I tested:
        - Adding tasks and checking them off
        - Reoccuring tasks
        - Scheduling conflicts and generating schedules properly
        - Sorting
        - Conflict detection
        - Filtering

- Why were these tests important?
    - These tests were important because they covered actions a normal user would do in the app. We need to make sure all actions in the app work as we and users expect them to.  

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - I am mostly confident that the scheduler works correctly, there was a few bugs I tried to fix myself but I am confident it covers mostly everything.
- What edge cases would you test next if you had more time?
    - I would test some overlapping scenarios, example being like two tasks with the exact same priority and duration and determining which one it picks, it should pick based on fifo, but this isnt confirmed. Also did not check for the date rollover at the end of the month. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - The whole process felt very smooth and rewarding. It was really enjoyable to see the features come to life and test them to make sure they worked as envisioned.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - If I could improve something it would be making the front end a bit more user friendly like adding the task completion next to the current task list and other front end stuff.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - I learned that AI is really good once it has a whole plan. Even if that means coming up with a plan using it, the context it gains makes the whole process much smoother.