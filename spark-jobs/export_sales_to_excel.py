"""
Spark Job 3: Export Postgres Data to Excel
This Spark job demonstrates:
- Reading data from Postgres
- Aggregating with Spark
- Exporting the result to an .xlsx file for downstream distribution (e.g. email)
"""
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count, round as _round


# SparkSubmitOperator runs in client deploy-mode, so this driver process actually
# executes inside the Airflow container (not spark-master/spark-worker) - use the
# Airflow container's mount path, the same one EmailOperator reads from.
OUTPUT_PATH = "/opt/spark-jobs/output/sales_report.xlsx"

def main():
    spark = SparkSession.builder.appName("ExportSalesToExcel").getOrCreate()

    print("=" * 50)
    print("Starting Sales Export to Excel Job")
    print("=" * 50)

    jdbc_url = "jdbc:postgresql://postgres:5432/airflow"
    connection_properties = {
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"
    }

    try:
        print("\nReading data from Postgres...")
        sales_df = spark.read.jdbc(
            url=jdbc_url,
            table="sample_sales",
            properties=connection_properties
        )

        print("\nAggregating by category...")
        summary_df = sales_df.groupBy("category").agg(
            _sum(col("price") * col("quantity")).alias("total_revenue"),
            avg("price").alias("avg_price"),
            _sum("quantity").alias("total_quantity"),
            count("*").alias("transaction_count")
        ).select(
            col("category"),
            _round(col("total_revenue"), 2).alias("total_revenue"),
            _round(col("avg_price"), 2).alias("avg_price"),
            col("total_quantity"),
            col("transaction_count")
        ).orderBy(col("total_revenue").desc())

        print("\nSales Summary by Category:")
        summary_df.show(truncate=False)

        # Excel export needs a single machine, so collect to the driver.
        # Fine for report-sized aggregates - do not do this with full-size raw tables.
        pandas_df = summary_df.toPandas()

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        pandas_df.to_excel(OUTPUT_PATH, index=False, sheet_name="Sales Summary", engine="openpyxl")

        print(f"\nExcel report written to {OUTPUT_PATH}")
        print("\n" + "=" * 50)
        print("Sales Export to Excel Job Completed Successfully")
        print("=" * 50)

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
