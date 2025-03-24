# Imports
from airflow import DAG, Dataset
from airflow.utils.dates import days_ago
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Define the DAG: consumer dag
dag = DAG(
    'data_consumer_dag',
    default_args={'start_date': days_ago(1)},
    schedule=[Dataset("<replace valid s3 path>")] # you can change this to multiple dataset,

#   We usually code cron-based (or time based) schedule_interval as below:
#   schedule_interval="0 23 * * *",
)

# Define the Task
load_table = SnowflakeOperator(
    task_id='data_consumer_task',
    sql='./sqls/xrate_sf.sql',
    snowflake_conn_id='snowflake_conn',
    dag=dag
)