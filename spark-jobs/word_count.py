"""
Spark Job 1: Simple Word Count
This is a basic Spark job that demonstrates:
- Creating sample data
- Performing transformations
- Computing word frequencies
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col, lower

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("WordCount") \
        .getOrCreate()
    
    print("=" * 50)
    print("Starting Word Count Job")
    print("=" * 50)
    
    # Sample text data
    sample_text = [
        ("Apache Spark is a unified analytics engine for large-scale data processing",),
        ("Spark provides high-level APIs in Java, Scala, Python and R",),
        ("Apache Airflow is a platform to programmatically author, schedule and monitor workflows",),
        ("Airflow pipelines are defined as code making them more maintainable",),
        ("Docker containers make it easy to package and deploy applications",)
    ]
    
    # Create DataFrame
    df = spark.createDataFrame(sample_text, ["text"])
    
    print("\nOriginal Text:")
    df.show(truncate=False)
    
    # Word count transformation
    words_df = df.select(explode(split(lower(col("text")), "\\s+")).alias("word"))
    
    word_count = words_df.groupBy("word") \
        .count() \
        .orderBy(col("count").desc())
    
    print("\nWord Count Results:")
    word_count.show(20, truncate=False)
    
    # Get total word count
    total_words = words_df.count()
    unique_words = word_count.count()
    
    print(f"\nStatistics:")
    print(f"Total words: {total_words}")
    print(f"Unique words: {unique_words}")
    
    print("\n" + "=" * 50)
    print("Word Count Job Completed Successfully")
    print("=" * 50)
    
    spark.stop()

if __name__ == "__main__":
    main()
