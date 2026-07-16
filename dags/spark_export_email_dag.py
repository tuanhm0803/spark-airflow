"""
Example DAG 3: Export Postgres Data to Excel and Email It
This DAG demonstrates:
1. Reading data from Postgres via Spark
2. Exporting the aggregated result to .xlsx
3. Emailing the report as an attachment through Airflow's SMTP backend

Requires SMTP credentials to be configured first - see secrets.env.example
and the "Email setup" section of README.md.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.email import EmailOperator

REPORT_PATH = "/opt/spark-jobs/output/sales_report.xlsx"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'spark_export_email_report',
    default_args=default_args,
    description='Read from Postgres, export to Excel, email the report',
    schedule_interval='@daily',
    catchup=False,
    tags=['spark', 'postgres', 'email'],
) as dag:

    create_table = PostgresOperator(
        task_id='create_sample_table',
        postgres_conn_id='postgres_default',
        sql="""
            DROP TABLE IF EXISTS sample_sales;
            CREATE TABLE sample_sales (
                id SERIAL PRIMARY KEY,
                product_name VARCHAR(100),
                category VARCHAR(50),
                price DECIMAL(10,2),
                quantity INT,
                sale_date DATE
            );

            INSERT INTO sample_sales (product_name, category, price, quantity, sale_date) VALUES
            ('Laptop', 'Electronics', 999.99, 5, '2024-01-15'),
            ('Mouse', 'Electronics', 25.99, 10, '2024-01-15'),
            ('Desk', 'Furniture', 299.99, 3, '2024-01-16'),
            ('Chair', 'Furniture', 199.99, 7, '2024-01-16'),
            ('Monitor', 'Electronics', 349.99, 4, '2024-01-17'),
            ('Keyboard', 'Electronics', 79.99, 8, '2024-01-17'),
            ('Bookshelf', 'Furniture', 149.99, 2, '2024-01-18');
        """
    )

    export_to_excel = SparkSubmitOperator(
        task_id='export_sales_to_excel',
        application='/opt/spark-jobs/export_sales_to_excel.py',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
        },
        verbose=True,
        packages='org.postgresql:postgresql:42.6.0',
    )

    email_report = EmailOperator(
        task_id='email_sales_report',
        to=['tuanhm0803@gmail.com', 'hiitsling@gmail.com'],
        subject='Sales Report - {{ ds }}',
        html_content='<p>Attached is the sales report for {{ ds }}.</p>',
        files=[REPORT_PATH],
    )

    create_table >> export_to_excel >> email_report
