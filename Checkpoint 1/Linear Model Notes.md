## Linear Model Notes
The following notes will help us figure out how we're going to complete this project.

### Quantifying Invisible Labor Model

#### Task Input:

Add new feature columns:
- Completion Time: FINISHED_TASK - TASK_STARTED (seconds)
  project
    Completion Time = assignment_duration_in_seconds - time_to_deadline_in_seconds
- Count of Number of Tasks for Invisible Labor = FINISHED_TASK - TASK_STARTED filtered on task_id
- TBD: Third Feature?
- TBD: Fourth Feature?

#### Output:
- Estimated Invisible Task Rate (Dollars): Fixed amount based on completion (e.g. $2.35)

Invisible Labor Time (10 s)    Invisible Labor Pay (X)
--------------------------- =  -----------------------------
Paid Labor Time (20s)          Paid Labor Pay ($2)

$20 for 1 task (paid labor)
Y (invisible labor costs for X tasks)
F1 (invisible tasks) = TASK_START to FINSHED_TASK = 20
F2 (invisible task duration)

$Y for F1, F2 tasks (invisible labor pay)
$Y for 20 tasks, 20 minutes (invisible labor pay)

### Features
task_id
count_invisible_labor_tasks
actual_duration_invisible_labor_tasks (TASK_START to FINISHED_TASK)
estimate_duration_invisible_labor_tasks = c4.project.assignment_duration_in_seconds (7200 - 2 hrs) (maybe: paid + invisible labor)
c4.project.requester_name - Categorical by requester

dataset with at least 3 workers needed

### Checkpoint Deliverables - EDA

#### Graphs (Compare Features to Each Other)
- Feature (X): Completion Time, Output (Y): Number of Tasks
- Other graphs needed


#### [DON'T USE]
```
David suggested:
invisible labor hourly rate = invisible labor time * (monetary reward/visible labor time)
```

```
# Task Completion Reward
- c4 (extra)
  - project."monetary_reward": {
      "currency_code": "USD",
      "amount_in_dollars": 2.33
      },
```

----------------------

### Classification Model
Output: 0 - Not Complete the Task, 1 - Complete the Task

This was discussed as another possible solution for a model for Checkpoint 1, however, we decided to go with a linear model instead.

---

## Research Paper Indicates

Invisible labor is defined as “unpaid activities that occur within the context of
paid employment that workers perform in response to requirements (either implicit or explicit) from
employers and that are crucial for workers to generate income, to obtain or retain their jobs, and to
further their careers, yet are often overlooked, ignored, and/or devalued by employers, consumers,
workers, and ultimately the legal system itself [15].”

The central question this work addresses is how much time do workers actually spend on invisible
work, and how does this affect their overall hourly wages? This is an important question not only
to ensure that workers receive a fair wage now but also to ensure that workers receive a fair wage
in the future. ****

**HIT** - Human Intelligence Task (AWS Mechanical Turk)

**Real Hourly Rate** = Paid Labor Hourly Rate - Invisbile Hourly Rate

### Quantifying Paid Labor
- When crowd worker was completing a HIT
- Amount of time the worker invested in completing the HIT
- Daily earnings that workers made from HITS (help quantify the monetary costs of invisible labor)
- Record times when worker accepts, finishes, and submits a HIT.
- Track when a tab about a HIT is in focus and record time period which worker is active (check for interactions: mouse movements, typing)
- Measure daily income each worker makes from HITs (query information from workers' MTurk dashboard)

### Quantifying Invisible Labor
- Detect and quantify all other activties that workers do aside from completing HITs.
- Detect when worker visits other part so the MTurk platform that are different from the HIT page tab.
  - Worker entered MTurk page to search for HITS.
  - Worker entered MTurk page for sending messages to requestors.
- Plugin tracks exact time when worker enters these pages
  - Plugin scrapes page to identify how worker interacted with page and identifies intervals of time when worker is active on pages. 
    - Active means user has page in focus and does any type of user interaction on page (mouse movements, scroll, clicks, keyboard typing).
  - Plugin (Page Crawler):
    - Detects the current MTurk domain page that the worker is on, as well as the status of the page (e.g., that the page is loaded, active, inactive, or closed).
    - The primary element that we use to detect whether the worker is completing paid labor or invisible labor.
  - Plugin (Background Process): 
    - Focuses on detecting the HITs that the worker is currently doing and identifying which she has finished. In order to accomplish this, the background process polls workers’ task queues on MTurk every 30 seconds. From the task queue, the background process obtains the metadata and status of all the HITs the worker has accepted to do.
    - Be able to better detect when the worker is completing HITs (some of them reside outside the MTurk platform) and also when the worker is multi-tasking (doing multiple HITs at the same time.)
  - Note that for most cases, we detect that a worker started a new activity when they loaded, focused, or changed their browser tab to a page on MTurk related to that particular type of invisible labor.
  - Similarly, the plugin considers that a worker paused or finished an activity when the worker changed to another tab, unloaded, blurred, or closed the MTurk page related to that particular activity

#### Defining the Data

Calculate Invisible Labor Time based on different tasks performed. 
- Managing Payments
- Hyper-vigilance (watch over requesters' profiles for newly posted work; searching for labor)
- Messaging Requestors

These dependent features (variables) mentioned above could be used to predict dependent variables like the following:

Feature
- Time spent on invisible labor

Output (Predictor)
- Adjusted median hourly pay due to invisible labor work performed
The central question this work addresses is how much time do workers actually spend on invisible
work, and how does this affect their overall hourly wages?

---




