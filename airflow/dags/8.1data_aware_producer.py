from airflow import DAG, Dataset  # Importing DAG and Dataset classes from Airflow
from airflow.providers.amazon.aws.transfers.http_to_s3 import HttpToS3Operator  # Importing the operator to transfer data from HTTP to S3
from airflow.utils.dates import days_ago  # Importing utility to get the date from one day ago
from airflow.models import Variable  # Importing Variable class to access Airflow variables

# Defining the DAG (Directed Acyclic Graph) for the data producer
dag = DAG(
    "data_producer_dag",  # Name of the DAG
    default_args={"start_date": days_ago(1)},  # Setting default arguments, including start date
    schedule_interval="0 23 * * *",  # Scheduling the DAG to run daily at 23:00
)

# Defining a task to transfer data from an HTTP endpoint to an S3 bucket (producer dag)
http_to_s3_task = HttpToS3Operator(
    task_id="data_producer_task",  # Unique identifier for the task
    endpoint=Variable.get("web_api_key"),  # Getting the API endpoint from Airflow variables
    s3_bucket="sleek-data",  # Specifying the S3 bucket to store the data
    s3_key="oms/xrate.json",  # Specifying the S3 key (path) for the data
    aws_conn_id="aws_conn",  # AWS connection ID for authentication
    http_conn_id=None,  # HTTP connection ID (not used in this case)
    replace=True,  # Setting to replace the existing file in S3 if it exists
    dag=dag,  # Associating the task with the defined DAG
    outlets=[Dataset("<replace valid s3 path>")]  # Defining the dataset that this task produces
)