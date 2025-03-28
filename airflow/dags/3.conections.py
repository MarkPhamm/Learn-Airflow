############################################

#          Connections Example              #

############################################

# Imports
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.email_operator import EmailOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


# Define the DAG
dag = DAG(
    'connections_demo',
    default_args={'start_date': days_ago(1)},
    schedule_interval='0 21 * * *',
    catchup=False
)

# Define the Task
load_table = SQLExecuteQueryOperator(
    task_id='load_table',
    sql='./sql/profit_uk.sql',
    conn_id='snowflake_conn_id',
    dag=dag
)

send_email = EmailOperator(
    task_id='send_email',
    to="{{ var.value.get('email') }}",
    subject='UK profit table load - Successful',
    html_content='UK Sales table to Profit table Load Completed',
    dag=dag,
)

# Define the Dependencies
load_table >> send_email