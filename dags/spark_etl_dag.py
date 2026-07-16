"""
Example DAG 2: Spark ETL with Postgres
This DAG demonstrates:
1. Reading data from Postgres
2. Processing with Spark
3. Writing results back to Postgres
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def check_postgres_connection():
    from airflow.hooks.postgres_hook import PostgresHook
    pg_hook = PostgresHook(postgres_conn_id='postgres_default')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"PostgreSQL version: {version}")
    cursor.close()
    conn.close()

with DAG(
    'spark_etl_postgres',
    default_args=default_args,
    description='ETL pipeline with Spark and Postgres',
    schedule_interval='@daily',
    catchup=False,
    tags=['spark', 'etl', 'postgres'],
) as dag:

    # Create sample table in Postgres
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

    check_connection = PythonOperator(
        task_id='check_postgres_connection',
        python_callable=check_postgres_connection
    )

    # Run Spark ETL job
    spark_etl_job = SparkSubmitOperator(
        task_id='spark_etl_job',
        application='/opt/spark-jobs/sales_aggregation.py',
        conn_id='spark_default',
        conf={
            'spark.master': 'spark://spark-master:7077',
        },
        verbose=True,
        packages='org.postgresql:postgresql:42.6.0'
    )

    # Verify results
    verify_results = PostgresOperator(
        task_id='verify_results',
        postgres_conn_id='postgres_default',
        sql="""
            SELECT * FROM sales_summary;
        """
    )

    create_table >> check_connection >> spark_etl_job >> verify_results
