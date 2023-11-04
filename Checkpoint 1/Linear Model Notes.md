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




