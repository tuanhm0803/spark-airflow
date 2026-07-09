# Quick Reference Card - Common Commands

## 🚀 Starting & Stopping

### Start all services
```powershell
docker-compose up -d
```

### Start with build (after changing Dockerfile)
```powershell
docker-compose up -d --build
```

### Stop all services
```powershell
docker-compose down
```

### Stop and remove all data (including database)
```powershell
docker-compose down -v
```

### Restart specific service
```powershell
docker-compose restart airflow-scheduler
docker-compose restart spark-master
```

## 📊 Monitoring

### View all service status
```powershell
docker-compose ps
```

### View logs (follow mode)
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f airflow-webserver
docker-compose logs -f spark-master
docker-compose logs -f postgres
```

### View last 100 lines of logs
```powershell
docker-compose logs --tail=100 airflow-scheduler
```

## 🔧 Accessing Containers

### Execute command in container
```powershell
# Airflow
docker-compose exec airflow-webserver bash

# Spark
docker-compose exec spark-master bash

# Postgres
docker-compose exec postgres bash
```

### Access Postgres database
```powershell
docker-compose exec postgres psql -U airflow -d airflow
```

## 📝 Postgres Queries

```sql
-- List all tables
\dt

-- View sample sales data
SELECT * FROM sample_sales;

-- View aggregated results
SELECT * FROM sales_summary;

-- Exit postgres
\q
```

## 🎯 Airflow Commands (in container)

```bash
# List DAGs
airflow dags list

# Trigger a DAG
airflow dags trigger spark_word_count

# Test a specific task
airflow tasks test spark_word_count spark_word_count_job 2024-01-01

# List connections
airflow connections list

# Create Spark connection
airflow connections add spark_default \
  --conn-type spark \
  --conn-host spark://spark-master \
  --conn-port 7077
```

## 🔥 Spark Commands (in container)

```bash
# Submit Spark job manually
spark-submit \
  --master spark://spark-master:7077 \
  /opt/spark-jobs/word_count.py

# Check Spark version
spark-submit --version

# Interactive PySpark shell
pyspark --master spark://spark-master:7077
```

## 🐛 Troubleshooting

### Rebuild everything from scratch
```powershell
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Check disk space
```powershell
docker system df
```

### Clean up Docker
```powershell
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune -f
```

### View resource usage
```powershell
docker stats
```

## 🌐 Web Interfaces

- **Airflow**: http://localhost:8080 (airflow/airflow)
- **Spark Master**: http://localhost:8081
- **Postgres**: localhost:5432 (airflow/airflow/airflow)

## 📁 Important Directories

- `./dags/` - Place Airflow DAG files here
- `./spark-jobs/` - Place Spark job files here
- `./logs/` - Airflow logs
- `./plugins/` - Custom Airflow plugins

## 🔄 Workflow for Adding New Jobs

1. Create Spark job in `spark-jobs/`
2. Create DAG file in `dags/`
3. Wait ~30 seconds for Airflow to detect new DAG
4. Enable DAG in Airflow UI
5. Configure any required connections
6. Trigger DAG manually or wait for schedule

## 📦 Adding Python Dependencies

1. Add package to `requirements.txt`
2. Rebuild Airflow image:
   ```powershell
   docker-compose up -d --build airflow-webserver airflow-scheduler
   ```

## 🔐 Changing Passwords

Edit `.env` file:
```
_AIRFLOW_WWW_USER_USERNAME=your_username
_AIRFLOW_WWW_USER_PASSWORD=your_password
```

Then recreate:
```powershell
docker-compose down
docker-compose up -d
```
