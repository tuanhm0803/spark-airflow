# Download PostgreSQL JDBC Driver
# Run this script to download the JDBC driver needed for Spark-Postgres integration

Write-Host "Downloading PostgreSQL JDBC Driver..." -ForegroundColor Yellow

# Create jars directory if it doesn't exist
$jarsDir = ".\jars"
if (-not (Test-Path $jarsDir)) {
    New-Item -ItemType Directory -Path $jarsDir | Out-Null
    Write-Host "Created jars directory" -ForegroundColor Green
}

# Download JDBC driver
$jdbcUrl = "https://jdbc.postgresql.org/download/postgresql-42.6.0.jar"
$jdbcPath = "$jarsDir\postgresql-42.6.0.jar"

try {
    Invoke-WebRequest -Uri $jdbcUrl -OutFile $jdbcPath
    Write-Host "✓ JDBC driver downloaded successfully to $jdbcPath" -ForegroundColor Green
    Write-Host "`nNote: You'll need to restart Spark services for the driver to be loaded" -ForegroundColor Yellow
    Write-Host "Run: docker-compose restart spark-master spark-worker" -ForegroundColor Cyan
} catch {
    Write-Host "✗ Error downloading JDBC driver: $_" -ForegroundColor Red
    Write-Host "`nAlternative: The driver will be automatically downloaded when Spark jobs run" -ForegroundColor Yellow
}
