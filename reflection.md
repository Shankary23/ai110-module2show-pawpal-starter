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
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

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

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
