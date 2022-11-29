from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'dw',
    'start_date': datetime(2021, 5, 9),
}

dag = DAG('timetable', description = 'spark test', catchup = False, schedule_interval = "@hourly", default_args = default_args)

s1 = SparkSubmitOperator(
    task_id = "spark-job",
    application = "./dags/spark-app.py",
    conn_id = "spark_default",
    dag = dag
)