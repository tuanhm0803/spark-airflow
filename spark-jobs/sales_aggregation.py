"""
Spark Job 2: Sales Data Aggregation with Postgres
This Spark job demonstrates:
- Reading data from Postgres
- Performing aggregations
- Writing results back to Postgres
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, avg, count, round as _round

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("SalesAggregation") \
        .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.6.0.jar") \
        .getOrCreate()
    
    print("=" * 50)
    print("Starting Sales Aggregation Job")
    print("=" * 50)
    
    # Postgres connection properties
    jdbc_url = "jdbc:postgresql://postgres:5432/airflow"
    connection_properties = {
        "user": "airflow",
        "password": "airflow",
        "driver": "org.postgresql.Driver"
    }
    
    try:
        # Read data from Postgres
        print("\nReading data from Postgres...")
        sales_df = spark.read.jdbc(
            url=jdbc_url,
            table="sample_sales",
            properties=connection_properties
        )
        
        print("\nSample Sales Data:")
        sales_df.show(10, truncate=False)
        
        # Perform aggregations
        print("\nPerforming aggregations by category...")
        
        sales_summary = sales_df.groupBy("category").agg(
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
        sales_summary.show(truncate=False)
        
        # Write results back to Postgres
        print("\nWriting results back to Postgres...")
        sales_summary.write.jdbc(
            url=jdbc_url,
            table="sales_summary",
            mode="overwrite",
            properties=connection_properties
        )
        
        # Calculate overall metrics
        total_revenue = sales_df.agg(
            _sum(col("price") * col("quantity")).alias("total")
        ).collect()[0]["total"]
        
        print(f"\nOverall Metrics:")
        print(f"Total Revenue: ${total_revenue:.2f}")
        print(f"Total Transactions: {sales_df.count()}")
        
        print("\n" + "=" * 50)
        print("Sales Aggregation Job Completed Successfully")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise
    finally:
        spark.stop()

if __name__ == "__main__":
    main()
