# CPSC 6300: Applied Data Science – Course Project (Online Workers)
Detecting working patterns from online workers and predicting task completion.

## Background
The rise of AI technologies has created a vast amount of work for independent workers. These jobs include activities such as image, text, and audio annotation, as well as audio transcription, completing surveys, and many other activities. The crowdsourcing platforms (i.e., Amazon Mechanical Turk, Yandex Toloka, etc.) offer microtasks to online workers from all over the world. This type of work is considered invisible work since it is not regulated, and few people know about it. The working patterns of these workers can be studied by analyzing telemetry data from workers completing tasks. This project aims to understand the working patterns of these workers and build AI models able to predict the activities they will take and finish. Project detailsLinks to an external site..

## Group Members
- Stephen Becker <sgbecke@g.clemson.edu>
- David Croft <dcroft@g.clemson.edu>
- Zachary Trabookis <ztraboo@clemson.edu>

## Installation
Please make sure to download and put the following telemetry information in the `/data` directory. We've excluded commiting this data to source control because of the size of the data.
- **Dataset Amazon Mechanical Turk (AMT)** – name file `amazon_mechanical_turk_records.csv`
  https://drive.google.com/file/d/1Ryv5yftTsrlt5UhmP77vB6Uz49nfpp-F/view?usp=share_link
- **Dataset Toloka Yandex** – name file `toloka_telemetry_db.csv`
  https://drive.google.com/file/d/1MvMk5UjfXI5zvOA8dXVtdjcPYbOQiaRD/view?usp=share_link

## Project Milestones and Final Project Deliverable
The following outlines what we needed to complete for this project. The following includes feature dataset used in all three checkpoints through our project and the final project submission files.

#### Feature Dataset
Please refer to the [`./data/cloudworker_tasks_adjusted.csv`](./data/cloudworker_tasks_adjusted.csv) that will be used in all checkpoints below.

#### Checkpoint 1: Transform Original Dataset Into Feature Set and Build Exploratory Data Analysis (EDA)
Please refer to the `./Checkpoint 1` directory. 
- **[checkpoint_1.ipynb](./Checkpoint%201/checkpoint_1.ipynb)** Used for EDA for the final feature set.

These two files are used to generate the final feature set used by all checkpoints. Note that they will take time to process the original datasets mentioned above. Only recommend running these if your to rebuild the [`./data/cloudworker_tasks_adjusted.csv`](./data/cloudworker_tasks_adjusted.csv).
- **online_workers_checkpoint1_aws_mturk.ipynb** Used to read in MTurk dataset and transform it to final feature set.
- **online_workers_checkpoint1_toloka.ipynb** Used to read in Toloka dataset and transform it to final feature set. This is not complete. Python multiprocessing package was started here to help speed up the time to process events from the original dataset.

#### Checkpoint 2: K-NN (K-Nearest Neighbor) Model used for predicting if a crowd worker would complete a task.
Please refer to the `./Checkpoint 2` directory. 
- **[checkpoint_2.ipynb](./Checkpoint%202/checkpoint_2.ipynb)** Used for generating a kNN model and evaluating it with confusion matrix.
 
#### Checkpoint 3: Support Vector Machine (SVN) Model used for predicting if a crowd worker would complete a task.
- **[checkpoint_3.ipynb](./Checkpoint%203/checkpoint_3.ipynb)** Used for generating a SVN model and evaluating it with confusion matrix.

#### Final Project Submission: LaTeX project files and PDF
Please refer to the `./Final Project Submission/` directory to locate main.tex LaTeX file used to build final PDF for submission. The PDF is a writeup that is composed of all three checkpoints above.
- **[cpsc-6300-final-project-submission.pdf](./Final%20Project%20Submission/cpsc-6300-final-project-submission.pdf)** The final report submitted for the class project.
- **[main.tex](./Final%20Project%20Submission/main.tex)** The final LaTeX project used to generate the final class project PDF. You can utilize [Texmaker](https://www.xm1math.net/texmaker/) cross-platform application to edit LaTeX.

## Project Background
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
