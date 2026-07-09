# Quick Start Script for Windows PowerShell

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Airflow + Spark + Postgres Setup" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Step 1: Create directories
Write-Host "`n[1/4] Creating required directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs", "plugins" | Out-Null
Write-Host "✓ Directories created" -ForegroundColor Green

# Step 2: Set environment variables
Write-Host "`n[2/4] Setting environment variables..." -ForegroundColor Yellow
$env:AIRFLOW_UID = "50000"
Write-Host "✓ AIRFLOW_UID set to 50000" -ForegroundColor Green

# Step 3: Build and start services
Write-Host "`n[3/4] Building and starting Docker services..." -ForegroundColor Yellow
Write-Host "This may take 5-10 minutes on first run..." -ForegroundColor Gray
docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Services started successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Error starting services" -ForegroundColor Red
    exit 1
}

# Step 4: Wait for services to be ready
Write-Host "`n[4/4] Waiting for services to initialize..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes..." -ForegroundColor Gray
Start-Sleep -Seconds 30

# Check service status
Write-Host "`n" + "=" * 60 -ForegroundColor Cyan
Write-Host "Service Status:" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
docker-compose ps

# Display access information
Write-Host "`n" + "=" * 60 -ForegroundColor Green
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

Write-Host "`nAccess your services:" -ForegroundColor White
Write-Host "  • Airflow UI: " -NoNewline; Write-Host "http://localhost:8080" -ForegroundColor Cyan
Write-Host "    Username: airflow" -ForegroundColor Gray
Write-Host "    Password: airflow" -ForegroundColor Gray
Write-Host "`n  • Spark UI:   " -NoNewline; Write-Host "http://localhost:8081" -ForegroundColor Cyan
Write-Host "`n  • Postgres:   " -NoNewline; Write-Host "localhost:5432" -ForegroundColor Cyan
Write-Host "    Username: airflow" -ForegroundColor Gray
Write-Host "    Password: airflow" -ForegroundColor Gray
Write-Host "    Database: airflow" -ForegroundColor Gray

Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "  1. Wait 2-3 minutes for Airflow to fully initialize" -ForegroundColor Yellow
Write-Host "  2. Open http://localhost:8080 and login" -ForegroundColor Yellow
Write-Host "  3. Configure connections (see README.md)" -ForegroundColor Yellow
Write-Host "  4. Enable and run the example DAGs" -ForegroundColor Yellow

Write-Host "`nUseful commands:" -ForegroundColor White
Write-Host "  • View logs:     docker-compose logs -f" -ForegroundColor Gray
Write-Host "  • Stop services: docker-compose down" -ForegroundColor Gray
Write-Host "  • Restart:       docker-compose restart" -ForegroundColor Gray

Write-Host "`nFor detailed instructions, see README.md" -ForegroundColor White
Write-Host "=" * 60 -ForegroundColor Green
