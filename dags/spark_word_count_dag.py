"""
Example DAG 1: Simple Spark Word Count
This DAG demonstrates how to submit a Spark job from Airflow
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def print_starting():
    print("Starting Spark Word Count Job")

def print_completed():
    print("Spark Word Count Job Completed")

with DAG(
    'spark_word_count',
    default_args=default_args,
    description='Simple Spark word count job',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['spark', 'example'],
) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=print_starting
    )

    spark_job = SparkSubmitOperator(
        task_id='spark_word_count_job',
        application='/opt/spark-jobs/word_count.py',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
        },
        verbose=True
    )

    end = PythonOperator(
        task_id='end',
        python_callable=print_completed
    )

    start >> spark_job >> end
