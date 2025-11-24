<#
.SYNOPSIS
    Deployment script for the Café Application
.DESCRIPTION
    This script automates the deployment process for the Café Application.
    It handles virtual environment setup, dependency installation, and database migrations.
.PARAMETER environment
    The deployment environment (development or production). Default is 'development'.
.PARAMETER migrate
    If specified, runs database migrations.
.EXAMPLE
    .\deploy.ps1 -environment production -migrate
#>

param(
    [string]$environment = "development",
    [switch]$migrate = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Print header
Write-Host "=== Café Application Deployment ===" -ForegroundColor Cyan
Write-Host "Environment: $environment" -ForegroundColor Yellow
if ($migrate) {
    Write-Host "Will run database migrations" -ForegroundColor Yellow
}

# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $exists = $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
    return $exists
}

# Check for Python
if (-not (Test-CommandExists python)) {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.8 or higher."
    exit 1
}

# Check Python version
$pythonVersion = python --version
if ($pythonVersion -notmatch "Python 3\.([8-9]|1[0-9])") {
    Write-Error "Python 3.8 or higher is required. Found: $pythonVersion"
    exit 1
}

# Create virtual environment if it doesn't exist
$venvPath = ".\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $venvPath
}

# Activate virtual environment
$activateScript = "$venvPath\Scripts\Activate.ps1"
if (-not (Test-Path $activateScript)) {
    Write-Error "Failed to find virtual environment activation script at $activateScript"
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
. $activateScript

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Set environment variables
$env:FLASK_APP = "wsgi.py"
$env:FLASK_ENV = $environment

# Run database migrations if requested
if ($migrate) {
    Write-Host "Running database migrations..." -ForegroundColor Yellow
    try {
        flask db upgrade
        Write-Host "Database migrations completed successfully" -ForegroundColor Green
    } catch {
        Write-Error "Failed to run database migrations: $_"
        exit 1
    }
}

# For production, use Gunicorn
if ($environment -eq "production") {
    Write-Host "Starting Gunicorn server..." -ForegroundColor Yellow
    
    # Check if Gunicorn is installed
    if (-not (pip list | Select-String "gunicorn")) {
        Write-Host "Installing Gunicorn..." -ForegroundColor Yellow
        pip install gunicorn
    }
    
    # Start Gunicorn
    Start-Process -NoNewWindow -FilePath "$venvPath\Scripts\gunicorn" -ArgumentList "--config gunicorn_config.py wsgi:app"
    Write-Host "Gunicorn server started in the background" -ForegroundColor Green
} else {
    # For development, use Flask's built-in server
    Write-Host "Starting development server..." -ForegroundColor Yellow
    Write-Host "Application will be available at: http://127.0.0.1:5000/" -ForegroundColor Cyan
    flask run
}

Write-Host "Deployment completed successfully!" -ForegroundColor Green
