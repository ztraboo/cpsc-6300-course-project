# CPSC 4300/6300: Applied Data Science – Course Project (Online Workers)
Detecting working patterns from online workers and predicting task completion.

## Background
The rise of AI technologies has created a vast amount of work for independent workers. These jobs include activities such as image, text, and audio annotation, as well as audio transcription, completing surveys, and many other activities. The crowdsourcing platforms (i.e., Amazon Mechanical Turk, Yandex Toloka, etc.) offer microtasks to online workers from all over the world. This type of work is considered invisible work since it is not regulated, and few people know about it. The working patterns of these workers can be studied by analyzing telemetry data from workers completing tasks. This project aims to understand the working patterns of these workers and build AI models able to predict the activities they will take and finish. Project detailsLinks to an external site..

## Group Members
- David Croft <dcroft@g.clemson.edu>
- Stephen Becker <sgbecke@g.clemson.edu>
- Zachary Trabookis <ztraboo@clemson.edu>

## Installation
Please make sure to download and put the following telemetry information in the `/data` directory. We've excluded commiting this data to source control because of the size of the data.
- **Dataset Amazon Mechanical Turk (AMT)** – name file (amazon_mechanical_turk_records.csv)
  https://drive.google.com/file/d/1Ryv5yftTsrlt5UhmP77vB6Uz49nfpp-F/view?usp=share_link
- **Dataset Toloka Yandex** – name file (toloka_telemetry_db.csv)
  https://drive.google.com/file/d/1MvMk5UjfXI5zvOA8dXVtdjcPYbOQiaRD/view?usp=share_link

## Project Details
https://docs.google.com/presentation/d/1z1HJ2x8hVosnpLJisYwAoEImRqHhc-n6RC123E-aeh4/edit?usp=sharing

### Slide Notes
The following are notes provided by the Project Details slides and shall provide guidance on how we approach this project.

#### Slide 3: Invisible Labor in Crowd Work
- Activities such as the unpaid time workers have to invest include the following:
  - Finding Work
  - Being "on-call"
  - Ready to do tasks (hypervigilance)
  - Figure out how to do jobs (lack of guidance)
  - Managing their payments
  - General logistics (e.g. login)

#### Slide 4: Understanding Invisible Labor
- In this project, we study computational mechanisms for understanding the invisible labor that exists in crowd work.
> Build models to understand metrics from this crowd work.

- Facilitating tools for cross-platform auditing is important as digital labor platforms have traditionally been black boxes. 
> Feed both telemetry datasets (Amazon Mechanical Turk, Yandex Toloka) into our models. Need transform this telemetry data into a common data set used by our model.

- Understanding how workers actually spend on invisible work and how does this affect their overall hourly wages can help to ensure fairer wages.
> Build models to identify patterns in the work performed and evaluate if the workers are underpaid, etc.
The submitted form work used in this crowd work platform(s) may not be enough information to address the working patterns from online workers and predicting task completion. May need to look at the data events presented to find out more information.

#### Slide 5: Predictive Models
Consider building out multiple models to address this slide. Changing the order here of work to complete because completion time may feed into recommendations of next activities to perform.

Predictive models can help to:

1. Completion time.
Recommended Model: Linear Regression
- What the task was?
- How many times they've navigated away from it. Count of number of invisible task between start/completed task.

2. Recommend what activities to perform next.
Recommended Model: Categorical (kNN)

3. What activities are not suitable/interesting for the worker.
Recommended Model: Categorical (kNN)

**Core**
- Predict task completion time using log entries of crowd worker tasks (e.g. changing tabs, submitting form)
