# Learn-Airflow
Open-source platform that empowers data professional to efficiently create, schedule and monitor Tasks and Workflows
* Pure Python 
* Robust Integration 
* Highly Scalable
* Rich Interface
* Open source/ Cost effective

Lesson 1: Intro to Airflow and first Airflow DAGs
## DAG (Directed Acyclic Graph)
* **Directed**: Dependencies have a specified direction
* **Acyclic**: No cycles or Loops
* **Graph**: Diagram that consist of Nodes and Edges

## Tasks, Operators, Parameters, Depedencies, and Schedules
DAG consist of one more muplitple tasks, each tasks is created using an operator
* **Task**: A unit of work that is executed by the Airflow scheduler. Each task represents a single step in a workflow and can be defined using various operators.
* **Operator**: A template/abstraction for defining a task in Airflow. Operators determine what kind of work is to be done, such as executing a Python function, running a Bash command, or interacting with external systems like databases or cloud services.
* **Parameters**: Key-value pairs that are passed to operators to customize their behavior. Parameters allow users to define specific inputs for tasks, enabling dynamic workflows that can adapt to different data osr execution contexts.
* **Dependencies**: Relationships between tasks that dictate the order in which they must be executed. Dependencies ensure that a task is not started until all of its upstream tasks have been successfully completed, thereby maintaining the integrity of the workflow.
* **Schedules**: A schedule defines the timing and frequency at which tasks are executed within a DAG. It determines when a task should run, allowing users to specify intervals (e.g., hourly, daily) or specific times for execution. Schedules are crucial for automating workflows and ensuring that tasks are performed consistently and reliably over time.

## Airflow Architecture
* **Webserver**: The user interface for Airflow, allowing users to monitor and manage workflows, view logs, and trigger tasks manually.
* **Database**: Stores metadata, task states, and configuration information necessary for the operation of the Airflow system.
* **Scheduler**: Responsible for scheduling the execution of tasks based on their dependencies and defined schedules, ensuring that tasks are executed in the correct order.
* **Executor**: The component that determines how and where tasks are executed. It can be configured to use different execution backends, such as LocalExecutor, CeleryExecutor, or KubernetesExecutor.
* **Workers**: Compute layers that run the tasks, interacting with data and performing the actual work defined in the tasks. Workers can be distributed across multiple machines to scale the execution of workflows.

## Docker
A containerization platform that allows developers to package applications and their dependencies into containers, ensuring that they run consistently across different environments. We will use Docker to run Airflow
* **Consistent**: Ensures that applications run the same way regardless of where they are deployed.
* **Portable**: Containers can be easily moved between different environments, such as development, testing, and production.
* **Repeatable**: Enables the same container image to be used multiple times, ensuring that deployments are predictable and reliable.

# Lesson 2: Tasks, Operators, Parameters, Depedencies, Schedules, Providers & airflow.cfg

## airflow.cfg
This is the configuration file for Apache Airflow, where various settings and parameters are defined to control the behavior of the Airflow environment. It includes configurations for the executor, database connection, logging, and other operational settings that dictate how tasks are scheduled and executed within the Airflow framework.

## Tasks in Airflows
A task is created by instantiating a specific operator and providing the necessary task-level parameters. Each task represents a single unit of work within a Directed Acyclic Graph (DAG) and can be defined using various operators, such as PythonOperator, BashOperator, and EmailOperator, among others. 

## Operators in Airflows
Operators in Apache Airflow are the building blocks of tasks within a Directed Acyclic Graph (DAG). They define what kind of work is to be performed and can be categorized into several types based on their functionality:

1. **Action Operators**: These operators execute a specific function or task. For instance:
   - **PythonOperator**: This operator allows you to execute Python functions as tasks. It is commonly used for running custom Python code, making it versatile for various data processing tasks.
     ```python
     from airflow import DAG
     from airflow.operators.python import PythonOperator
     from airflow.utils.dates import days_ago

     def my_python_function():
         print("Hello from PythonOperator!")

     dag = DAG(
         'example_dag',
         default_args={'start_date': days_ago(1)},
         schedule_interval='@daily',
     )

     python_task = PythonOperator(
         task_id='run_my_python_function',
         python_callable=my_python_function,
         dag=dag,
     )
     ```
   - **BashOperator**: This operator is used to execute bash commands or scripts. It is useful for tasks that require shell commands, such as file manipulation or executing scripts in a Unix-like environment.
     ```python
     from airflow import DAG
     from airflow.operators.bash import BashOperator
     from airflow.utils.dates import days_ago

     dag = DAG(
         'example_bash_dag',
         default_args={'start_date': days_ago(1)},
         schedule_interval='@daily',
     )

     bash_task = BashOperator(
         task_id='run_bash_command',
         bash_command='echo "Hello from BashOperator!"',
         dag=dag,
     )
     ```
   - **Azure DataFactory Run Pipeline Operator**: This operator is used to execute Azure Data Factory pipelines.
     ```python
     from airflow import DAG
     from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator
     from airflow.utils.dates import days_ago

     dag = DAG(
         'example_azure_dag',
         default_args={'start_date': days_ago(1)},
         schedule_interval='@daily',
     )

     azure_pipeline_task = AzureDataFactoryRunPipelineOperator(
         task_id='run_azure_pipeline',
         pipeline_name='my_pipeline',
         azure_data_factory_conn_id='my_azure_data_factory',
         dag=dag,
     )
     ```

2. **Transfer Operators**: These operators are used for moving data from one place to another. An excellent example of this is:
   - **S3ToRedshiftOperator**: It moves data from Amazon S3 to Amazon Redshift.
     ```python
     from airflow import DAG
     from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
     from airflow.utils.dates import days_ago

     dag = DAG(
         's3_to_redshift_dag',
         default_args={'start_date': days_ago(1)},
         schedule_interval='@daily',
     )

     transfer_task = S3ToRedshiftOperator(
         task_id='transfer_s3_to_redshift',
         schema='public',
         table='my_table',
         s3_bucket='my_bucket',
         s3_key='data/my_data.csv',
         copy_options=['CSV'],
         aws_conn_id='aws_default',
         redshift_conn_id='redshift_default',
         dag=dag,
     )
     ```

3. **Sensor Operators**: These operators wait for a specific condition to be met before triggering the subsequent tasks in the workflow. Examples include:
   - **S3KeySensor**: This sensor waits for one or more files to be created in an S3 bucket.
     ```python
     from airflow import DAG
     from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
     from airflow.utils.dates import days_ago

     dag = DAG(
         's3_sensor_dag',
         default_args={'start_date': days_ago(1)},
         schedule_interval='@daily',
     )

     wait_for_file = S3KeySensor(
         task_id='wait_for_s3_file',
         bucket_name='my_bucket',
         bucket_key='data/my_data.csv',
         aws_conn_id='aws_default',
         poke_interval=10,
         timeout=60 * 60 * 5,
         soft_fail=True,
         dag=dag,
     )
     ```
   - **AWS Redshift Cluster Sensor**: This sensor waits for a Redshift cluster to reach a specific status.

4. **DummyOperator**: This operator does nothing and is often used as a placeholder in a DAG. It can help in structuring workflows and managing dependencies without performing any actual work.
   ```python
   from airflow import DAG
   from airflow.operators.dummy import DummyOperator
   from airflow.utils.dates import days_ago

   dag = DAG(
       'dummy_operator_dag',
       default_args={'start_date': days_ago(1)},
       schedule_interval='@daily',
   )

   start_task = DummyOperator(
       task_id='start',
       dag=dag,
   )
   ```

5. **BranchPythonOperator**: This operator allows for branching logic in workflows. It can be used to decide which path to take in a DAG based on certain conditions, enabling dynamic task execution.
   ```python
   from airflow import DAG
   from airflow.operators.python import BranchPythonOperator
   from airflow.utils.dates import days_ago

   def choose_branch():
       return 'branch_a'  # Logic to choose the branch

   dag = DAG(
       'branch_operator_dag',
       default_args={'start_date': days_ago(1)},
       schedule_interval='@daily',
   )

   branching_task = BranchPythonOperator(
       task_id='branching_task',
       python_callable=choose_branch,
       dag=dag,
   )
   ```

6. **SubDagOperator**: This operator allows you to define a sub-DAG within a parent DAG. It is useful for organizing complex workflows into smaller, manageable pieces.
   ```python
   from airflow import DAG
   from airflow.operators.subdag import SubDagOperator
   from airflow.utils.dates import days_ago

   def subdag(parent_dag_name, child_dag_name, args):
       dag_subdag = DAG(
           dag_id=child_dag_name,
           default_args=args,
           schedule_interval='@daily',
       )
       # Define tasks for the subdag here
       return dag_subdag

   dag = DAG(
       'subdag_operator_dag',
       default_args={'start_date': days_ago(1)},
       schedule_interval='@daily',
   )

   subdag_task = SubDagOperator(
       task_id='subdag_task',
       subdag=subdag('subdag_operator_dag', 'subdag_task', {'start_date': days_ago(1)}),
       dag=dag,
   )

## Operators vs Tasks
An operator can be viewed as a blueprint or design template, while tasks are the concrete implementations derived from that blueprint. In terms of Python or object-oriented programming, an operator represents a class, and tasks are instances (or objects) created from that class.

## Dependencies in Airflow
In Apache Airflow, managing task dependencies is crucial for ensuring that tasks are executed in the correct order. Here are some methods to define dependencies:

1. **Bitwise Operators**: You can use bitwise operators (`&` for "and", `|` for "or") to define dependencies between tasks in a more concise manner. For example, `task1 >> task2` can be expressed as `task1.set_downstream(task2)`. 
   - **Example**: 
     ```python
     task1 >> task2  # Using bitwise operator
     task1.set_downstream(task2)  # Using set_downstream method
     ```

2. **Set Upstream and Set Downstream Methods**: The `set_upstream()` and `set_downstream()` methods allow you to explicitly define the order of task execution. For instance, `task1.set_downstream(task2)` ensures that `task2` runs after `task1`.
   - **Example**: 
     ```python
     task2.set_upstream(task1)  # Ensures task1 runs before task2
     ```

3. **Chain Function**: The `chain()` function from the `airflow.utils.dag` module provides a convenient way to set multiple dependencies at once. For example, `chain(task1, task2, task3)` sets `task1` to run before `task2`, which in turn runs before `task3`.
   - **Example**: 
     ```python
     from airflow.utils.dag import chain
     chain(task1, task2, task3)  # Sets task1 -> task2 -> task3
     ```

4. **TaskFlow API**: The TaskFlow API simplifies the creation of tasks and their dependencies using Python decorators. By using the `@dag` and `@task` decorators, you can define a DAG and its tasks in a more intuitive way, automatically managing dependencies based on the function calls.
   - **Example**: 
     ```python
     from airflow.decorators import dag, task

     @dag(schedule_interval='@daily', start_date=days_ago(1))
     def my_dag():
         @task
         def task1():
             pass

         @task
         def task2():
             pass

         task1() >> task2()  # Automatically manages dependencies
     ```

# Variables
Variables are small storage containers for values that can be reused throughout tasks. They are essentially key-value pairs, where the variable name holds a specific value.
* **Regular Variable**: The value can be a standard string.
* **JSON Variable**: The value is formatted as a JSON string.
To create variables, navigate to the admin panel and select "Create Variables."

## Advantages of Variables
* **Ease of Change Implementation**: Modifications can be made easily without altering the code.
* **Environment Specificity**: Variables can be tailored for different environments.
* **Security**: Automatically detects and manages sensitive information.
* **Dynamic DAGs**: Useful for creating DAGs that can adapt to specific dates or conditions.

# Connection
Connections in Apache Airflow are essential configuration objects that store the necessary details required to establish connections to external systems, such as databases, cloud services, and APIs. Each connection is defined by a set of parameters, including the connection ID, host, schema, login credentials, and any additional options specific to the service being connected to. 

To create a new connection, navigate to the Admin panel, select the "Connections" option, and then click on "Create." Here, you can define various types of connections, such as those for Amazon Redshift or Snowflake. You will need to enter the required information, including the connection ID, host address, username, password, and any other relevant parameters. After entering the details, it is crucial to test the connection to ensure that it can successfully communicate with the external system before integrating it into your DAG.

## Benefits of Connections
* **Reusability and Maintainability**: Connections can be reused across multiple DAGs and tasks, reducing redundancy and simplifying maintenance. If a connection's details change, you only need to update it in one place.
* **Environment Specificity**: Connections can be tailored for different environments (e.g., development, testing, production), allowing for seamless transitions and configurations without modifying the DAG code.
* **Ease of Implementing Changes**: Modifications to connection parameters can be made easily through the Airflow UI, enabling quick adjustments without the need to alter the underlying codebase.
* **Security**: Connections help manage sensitive information, such as passwords and API keys, securely. Airflow provides mechanisms to encrypt these details, ensuring that they are not exposed in the code or logs.

# Sensors
Airflow sensors are a specialized type of operator designed to monitor specific conditions until they are met.

These sensors periodically check for the specified condition. Once the condition is satisfied, the associated task is marked as successful, allowing downstream tasks to proceed. Sensors enhance the event-driven nature of your DAGs, making them suitable for scenarios such as waiting for a file to be created, a database table to be updated, or an external API to become available.

* **poke_interval:** The interval (in seconds) at which the sensor checks for the specified condition.
* **mode:** Determines the execution mode of the sensor, such as "poke" or "reschedule".
* **timeout:** The maximum time (in seconds) the sensor will wait for the condition to be met before failing.
* **soft_fail:** If set to true, the task will not fail the DAG if the sensor times out.

Example: The first task employs the S3KeySensor, which waits for a file to appear in an AWS S3 bucket. Once the file is detected, the subsequent task loads the file into a Snowflake table.

# Deferrable Operators & Triggers
By default, sensors work in 'poke' mode, which worker slot continuously allocated, even if the task is inactive or in sleep mode. Schedule allow worker slot at fixed interval. More worker slot means higher cost

**`Deferrable operators`** are designed to suspend their execution and completely free up the worker slot when they need to wait for a condition to be met. While in a suspended or deferred state, they do not occupy a worker slot, allowing for more efficient resource utilization. For instance, if you have 100 sensors, each would typically occupy a worker slot, leading to a one-to-one mapping. However, with deferrable operators, a single trigger can manage multiple sensors asynchronously, efficiently handling up to 100 sensors simultaneously without consuming individual worker slots for each one.


```python
from airflow import DAG
from airflow.providers.common.sql.sensors.sql import SqlSensor
from airflow.providers.common.sql.triggers.sql import SqlTrigger
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.common.sql.sensors.sql import SqlSensorAsync
from datetime import datetime, timedelta

# Define default_args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    'deferrable_operator_example',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

# Normal SQL Sensor (Blocking Worker Slot)
sql_sensor = SqlSensor(
    task_id='blocking_sql_sensor',
    conn_id='postgres_default',
    sql='SELECT COUNT(*) FROM my_table WHERE status = "ready";',
    mode='poke',  # Continuously runs, occupying a worker slot
    poke_interval=10,  # Checks every 10 seconds
    timeout=600,  # Timeout after 10 minutes
    dag=dag
)

# Deferrable SQL Sensor (Non-blocking)
async_sql_sensor = SqlSensorAsync(
    task_id='non_blocking_sql_sensor',
    conn_id='postgres_default',
    sql='SELECT COUNT(*) FROM my_table WHERE status = "ready";',
    mode='reschedule',  # Frees worker slot while waiting
    poke_interval=10,
    timeout=600,
    dag=dag
)

# Postgres Task (Executed after condition is met)
process_data = PostgresOperator(
    task_id='process_data',
    postgres_conn_id='postgres_default',
    sql="UPDATE my_table SET processed = TRUE WHERE status = 'ready';",
    dag=dag
)

# Define task dependencies
async_sql_sensor >> process_data
```

# Trigger vs Sensors
* **Sensors** are a type of operator that continuously check for a certain condition to be met before allowing downstream tasks to proceed. They are typically used for scenarios like waiting for a file to appear in a specific location, a database record to be updated, or an external API to become available. Sensors operate in 'poke' mode by default, which means they periodically check the condition at defined intervals (poke_interval) until the condition is satisfied or a timeout occurs. This can lead to inefficient resource usage, as each sensor occupies a worker slot while it is active.

* **Triggers**, on the other hand, are part of the deferrable operators in Airflow. They allow tasks to suspend their execution and free up the worker slot while waiting for a condition to be met. This is particularly useful for optimizing resource utilization, as it enables a single trigger to manage multiple conditions asynchronously without consuming individual worker slots for each one. When the condition is met, the trigger wakes up the task, allowing it to continue execution.

# Xcom
# XCom in Apache Airflow

## Overview
**XCom (Cross-Communication)** is a feature in Apache Airflow that allows tasks to exchange data with each other. This capability is crucial in workflows where the output of one task needs to be used as the input for another. XComs are stored in Airflow's metadata database and can be used to pass small pieces of data between tasks.

## XCom Push
The **XCom push** mechanism is used to send data from one task to another. Data is pushed into the XCom table in Airflow's metadata database. You can push data using the `xcom_push` method or by returning a value from a Python task:

#### Using `xcom_push` Method
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def push_data(ti):
    ti.xcom_push(key='message', value='Hello from XCom!')

dag = DAG(
    'xcom_example',
    schedule_interval=None,
    start_date=datetime(2024, 3, 20),
    catchup=False
)

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_data,
    provide_context=True,
    dag=dag
)
```

#### Using the Return Value of a Python Task
```python
def push_data():
    return "Hello from XCom!"

push_task = PythonOperator(
    task_id='push_task',
    python_callable=push_data,
    dag=dag
)
```
In this case, Airflow automatically pushes the returned value to XCom with the key `return`.

## XCom Pull
The **XCom pull** mechanism retrieves data stored in XCom. This allows downstream tasks to access data pushed by upstream tasks. You can pull data using the `xcom_pull` method:

#### Using `xcom_pull` in a Python Task
```python
def pull_data(ti):
    message = ti.xcom_pull(task_ids='push_task', key='message')
    print(f"Received message: {message}")

pull_task = PythonOperator(
    task_id='pull_task',
    python_callable=pull_data,
    provide_context=True,
    dag=dag
)
```

#### Using `xcom_pull` with Default Key (`return`)
If data was pushed using the return value of a Python function, it can be pulled as follows:
```python
message = ti.xcom_pull(task_ids='push_task', key='return')
```

## XCom Use Cases
- **Data Sharing Between Tasks**: Tasks can exchange values without using external storage.
- **Dynamic Task Execution**: The result of one task can determine the behavior of another.
- **Triggering Conditional Logic**: Use XCom values to control the execution of downstream tasks.

## Considerations
- XCom is stored in the Airflow database and should be used for small data values.
- For larger data, it's recommended to use cloud storage solutions or databases.
- XCom values are serialized as JSON, so only serializable objects can be stored.

For example, if the first task generates a file, the second task can upload that file to an S3 bucket. In our current setup, we have the 'replace' parameter set to true, which means that each time we run this DAG, the new file overwrites the previous one in S3. However, if this DAG runs multiple times a day, the business may want to keep a history of the exchange rate files. Since the file name created in Task One is not automatically known to Task Two, we can use XCom to bridge this gap.

In Task One, we use the XCom push feature to store the generated file name in Airflow’s metadata database. Then, in Task Two, we can retrieve that file name using the XCom pull feature, ensuring the correct file is uploaded to S3.

It's important to note that XComs are intended for passing small amounts of data between tasks, such as file names, task metadata, dates, or single-value query results. For larger datasets, consider using a custom XCom backend or intermediary data storage solutions to manage the data more effectively.

# Hooks  
Hooks are **pre-built Python classes** that simplify interactions with external systems and services.  

For example, the **S3Hook** (part of the AWS provider package) provides methods to interact with S3:  
- `create_bucket()`: Creates an Amazon S3 bucket  
- `load_string()`: Uploads a string as a file in S3  
- `delete_objects()`: Deletes an S3 file  

## Why Use Hooks?  
Hooks abstract low-level Python code, making it easier to interact with external services. Instead of writing complex logic, you can **import and use pre-built hooks** from Airflow’s provider packages.  

## Hooks vs. Operators  
Both are Python classes, but:  
- **Hooks** handle low-level interactions with external services.  
- **Operators** wrap around Hooks and provide task-level abstraction.  

For example, an AWS operator may use the **S3Hook’s** `copy_object()` method internally.  

## When to Use Hooks vs. Operators  
- **Use an Operator** if one exists for your task.  
- **Use a Hook** if no operator is available.  
- **Write custom Python code** if neither a hook nor an operator exists.  

## Using Hooks in DAGs  
Example: Transform an S3 file and re-upload it.  
1. Read the file using `read_key()` from S3Hook  
2. Apply transformations  
3. Upload it back using `load_string()`  

Within the DAG, call the transformation function with the bucket name, source file, and target file.

# Airflow Datasets   
Datasets enable **data-aware scheduling**, allowing DAGs to trigger based on the availability of files or datasets instead of time-based scheduling.  

A **dataset** is a logical representation of underlying data. You can create a dataset in Airflow by instantiating the `Dataset` class, using either:  
- A **complete URI** (e.g., `s3://bucket/exchange_rates.csv`)  
- A **descriptive string** (e.g., `"exchange_rates"`)  

Airflow does not access or validate the data—datasets serve as identifiers for establishing **producer-consumer DAG relationships**.  

## Benefits of Datasets  
- **Cross-DAG dependencies**: Connect DAGs that rely on shared data.  
- **Flexible scheduling**: Trigger DAGs dynamically when data is available.  
- **Reduced Airflow costs**: Unlike sensors, datasets do not use worker slots.  

## Producer and Consumer DAGs  
A **Producer DAG** updates a dataset using the `outlets` parameter.  
A **Consumer DAG** is scheduled based on dataset availability.  

### Example  
- **Producer DAG**: Ingests exchange rate data into an S3 bucket.  
- **Consumer DAG**: Transforms the data and loads it into Snowflake when new data is available.  

## Viewing Datasets in Airflow  
- **Datasets Tab**: Shows dataset triggers and history.  
- **DAG Dependencies View**: Visualizes cross-DAG relationships.  

## Triggering a DAG Based on Multiple Datasets  
A DAG can be scheduled based on **multiple producer DAGs or datasets** by listing them as comma-separated values. The DAG runs once all producer tasks complete successfully. 
