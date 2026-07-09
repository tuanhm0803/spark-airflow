# Airflow + Spark + Postgres Docker Setup

This project provides a complete Docker-based setup for learning Apache Airflow with Apache Spark and PostgreSQL integration.

## 📋 What's Included

- **Apache Airflow 2.8.1**: Workflow orchestration platform
- **Apache Spark 3.5**: Distributed data processing engine
- **PostgreSQL 13**: Relational database
- **2 Example DAGs**: Ready-to-run workflow examples
- **2 Example Spark Jobs**: Sample PySpark applications

## 🏗️ Architecture

```
├── Airflow Webserver (Port 8080)
├── Airflow Scheduler
├── Spark Master (Port 8081)
├── Spark Worker
└── PostgreSQL (Port 5432)
```

## 📁 Project Structure

```
spark&airflow/
├── dags/                           # Airflow DAG definitions
│   ├── spark_word_count_dag.py    # Simple word count example
│   └── spark_etl_dag.py            # ETL with Postgres example
├── spark-jobs/                     # Spark application files
│   ├── word_count.py               # Word count PySpark job
│   └── sales_aggregation.py       # Sales ETL PySpark job
├── logs/                           # Airflow logs (auto-created)
├── plugins/                        # Airflow plugins (auto-created)
├── docker-compose.yml              # Docker services configuration
├── Dockerfile                      # Custom Airflow image
├── requirements.txt                # Python dependencies
└── .env                            # Environment variables
```

## 🚀 Getting Started

### Prerequisites

- Docker Desktop installed
- At least 4GB RAM allocated to Docker
- Docker Compose v2.0 or higher

### Step 1: Initialize the Environment

On Windows PowerShell:
```powershell
# Navigate to project directory
cd "d:\Small_Projects\spark&airflow"

# Create required directories
mkdir logs, plugins -Force

# Set environment variable for Airflow UID
$env:AIRFLOW_UID = 50000
```

### Step 2: Build and Start Services

```powershell
# Build custom Airflow image and start all services
docker-compose up -d --build
```

This will start:
- Postgres database
- Airflow webserver and scheduler
- Spark master and worker

**Note**: First startup may take 5-10 minutes to download images and initialize.

### Step 3: Verify Services

Check that all services are running:
```powershell
docker-compose ps
```

All services should show "running" status.

### Step 4: Access the Web Interfaces

**Airflow UI:**
- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

**Spark UI:**
- URL: http://localhost:8081
- No authentication required

## 🎯 Running the Example DAGs

### Example 1: Spark Word Count

This DAG demonstrates basic Spark job submission from Airflow.

1. Open Airflow UI (http://localhost:8080)
2. Find the DAG: `spark_word_count`
3. Toggle it ON (switch on the left)
4. Click the "Play" button to trigger manually
5. Watch the progress in the Graph view
6. Check Spark UI (http://localhost:8081) to see the job execution

**What it does:**
- Creates sample text data
- Counts word frequencies using Spark
- Displays results in logs

### Example 2: Spark ETL with Postgres

This DAG demonstrates a complete ETL pipeline.

1. First, configure Postgres connection in Airflow:
   - Go to Admin > Connections
   - Edit `postgres_default` connection:
     - Host: `postgres`
     - Schema: `airflow`
     - Login: `airflow`
     - Password: `airflow`
     - Port: `5432`

2. Configure Spark connection:
   - Go to Admin > Connections
   - Add new connection `spark_default`:
     - Connection Type: `Spark`
     - Host: `spark://spark-master`
     - Port: `7077`

3. Find the DAG: `spark_etl_postgres`
4. Toggle it ON and trigger manually

**What it does:**
- Creates a sample sales table in Postgres
- Reads data using Spark
- Performs aggregations by category
- Writes results back to Postgres

## 🔍 Viewing Logs and Results

### Airflow Logs
- In Airflow UI, click on any task > Log button
- Or check the `logs/` directory

### Spark Logs
- Access Spark UI at http://localhost:8081
- View job details and execution metrics

### Postgres Data
Connect to Postgres to see the data:
```powershell
docker-compose exec postgres psql -U airflow -d airflow
```

Then run SQL queries:
```sql
-- View sample sales data
SELECT * FROM sample_sales;

-- View aggregated results
SELECT * FROM sales_summary;
```

## 🛠️ Useful Commands

### Restart Services
```powershell
docker-compose restart
```

### View Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f airflow-scheduler
docker-compose logs -f spark-master
```

### Stop Services
```powershell
docker-compose down
```

### Stop and Remove All Data
```powershell
docker-compose down -v
```

### Access Container Shell
```powershell
# Airflow
docker-compose exec airflow-webserver bash

# Spark Master
docker-compose exec spark-master bash

# Postgres
docker-compose exec postgres bash
```

## 📚 Learning Path

1. **Start Simple**: Run the word count DAG to understand basic Airflow-Spark integration
2. **Understand ETL**: Run the ETL DAG to see how data flows between Postgres and Spark
3. **Modify Jobs**: Edit the Spark jobs in `spark-jobs/` directory and re-run DAGs
4. **Create New DAGs**: Copy existing DAGs and modify them for your use cases
5. **Experiment**: Try adding new operators, scheduling intervals, or dependencies

## 🐛 Troubleshooting

### Services Won't Start
- Ensure Docker Desktop is running
- Check available RAM (need at least 4GB)
- Run: `docker-compose logs` to see errors

### Airflow UI Not Loading
- Wait 2-3 minutes after starting (initialization takes time)
- Check: `docker-compose logs airflow-webserver`

### DAGs Not Appearing
- DAGs appear within 30 seconds to 1 minute
- Check for Python syntax errors: `docker-compose logs airflow-scheduler`
- Ensure files are in the `dags/` directory

### Spark Jobs Failing
- Check Spark Master is running: http://localhost:8081
- Verify Spark connection in Airflow UI (Admin > Connections)
- Check Spark job logs in Airflow task logs

### Postgres Connection Errors
- Verify postgres service is healthy: `docker-compose ps postgres`
- Ensure connection details are correct in Airflow UI
- Test connection: `docker-compose exec postgres psql -U airflow -d airflow`

## 📖 Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [PySpark API Reference](https://spark.apache.org/docs/latest/api/python/)
- [Airflow Spark Provider](https://airflow.apache.org/docs/apache-airflow-providers-apache-spark/stable/)

## 🎓 Next Steps

1. **Learn Airflow Concepts**:
   - DAGs, Tasks, Operators
   - Task dependencies and scheduling
   - XComs for data passing

2. **Explore Spark**:
   - DataFrames and Datasets
   - Transformations and Actions
   - Spark SQL

3. **Build Your Own Pipelines**:
   - Create custom DAGs for your use cases
   - Integrate with other data sources
   - Add data quality checks

## 📄 License

This is a learning project. Feel free to modify and use as needed!

---

**Happy Learning! 🚀**
