# Learn-Airflow
Open-source platform that empowers data professional to efficiently create, schedule and monitor Tasks and Workflows
* Pure Python 
* Robust Integration 
* Highly Scalable
* Rich Interface
* Open source/ Cost effective

# DAG (Directed Acyclic Graph)
* **Directed**: Dependencies have a specified direction
* **Acyclic**: No cycles or Loops
* **Graph**: Diagram that consist of Nodes and Edges

# Tasks, Operators, Parameters, Depedencies, and Schedules
DAG consist of one more muplitple tasks, each tasks is created using an operator
* **Task**: A unit of work that is executed by the Airflow scheduler. Each task represents a single step in a workflow and can be defined using various operators.
* **Operator**: A template/abstraction for defining a task in Airflow. Operators determine what kind of work is to be done, such as executing a Python function, running a Bash command, or interacting with external systems like databases or cloud services.
* **Parameters**: Key-value pairs that are passed to operators to customize their behavior. Parameters allow users to define specific inputs for tasks, enabling dynamic workflows that can adapt to different data osr execution contexts.
* **Dependencies**: Relationships between tasks that dictate the order in which they must be executed. Dependencies ensure that a task is not started until all of its upstream tasks have been successfully completed, thereby maintaining the integrity of the workflow.
* **Schedules**: A schedule defines the timing and frequency at which tasks are executed within a DAG. It determines when a task should run, allowing users to specify intervals (e.g., hourly, daily) or specific times for execution. Schedules are crucial for automating workflows and ensuring that tasks are performed consistently and reliably over time.

# Airflow Architecture
* **Webserver**: The user interface for Airflow, allowing users to monitor and manage workflows, view logs, and trigger tasks manually.
* **Database**: Stores metadata, task states, and configuration information necessary for the operation of the Airflow system.
* **Scheduler**: Responsible for scheduling the execution of tasks based on their dependencies and defined schedules, ensuring that tasks are executed in the correct order.
* **Executor**: The component that determines how and where tasks are executed. It can be configured to use different execution backends, such as LocalExecutor, CeleryExecutor, or KubernetesExecutor.
* **Workers**: Compute layers that run the tasks, interacting with data and performing the actual work defined in the tasks. Workers can be distributed across multiple machines to scale the execution of workflows.

# Docker
A containerization platform that allows developers to package applications and their dependencies into containers, ensuring that they run consistently across different environments. We will use Docker to run Airflow
* **Consistent**: Ensures that applications run the same way regardless of where they are deployed.
* **Portable**: Containers can be easily moved between different environments, such as development, testing, and production.
* **Repeatable**: Enables the same container image to be used multiple times, ensuring that deployments are predictable and reliable.

