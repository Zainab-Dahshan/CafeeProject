<#
.SYNOPSIS
    Deployment script for the Café Application
.DESCRIPTION
    This script automates the deployment process for the Café Application.
    It handles virtual environment setup, dependency installation, database migrations,
    and production server setup.

.PARAMETER Environment
    The deployment environment (development, staging, production). Default is 'development'.

.PARAMETER Migrate
    If specified, runs database migrations.

.PARAMETER InstallDeps
    If specified, installs/updates Python dependencies.

.PARAMETER CreateAdmin
    If specified, creates an admin user.

.EXAMPLE
    # Development deployment with migrations
    .\deploy.ps1 -Environment development -Migrate -InstallDeps

    # Production deployment
    .\deploy.ps1 -Environment production -Migrate -InstallDeps
#>

param(
    [ValidateSet('development', 'staging', 'production')]
    [string]$Environment = "development",
    
    [switch]$Migrate = $false,
    [switch]$InstallDeps = $false,
    [switch]$CreateAdmin = $false
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Import required modules
Import-Module "$PSScriptRoot\deploy\deploy-utils.ps1" -ErrorAction SilentlyContinue

# Set environment variables
$env:FLASK_ENV = $Environment
if ($Environment -eq "production") {
    $env:FLASK_CONFIG = "production"
}

# Print header
Write-Host "=== Café Application Deployment ===" -ForegroundColor Cyan
Write-Host "Environment: $Environment" -ForegroundColor Yellow
Write-Host "Current directory: $PSScriptRoot" -ForegroundColor Gray

# Check for required commands
$requiredCommands = @('python', 'pip')
foreach ($cmd in $requiredCommands) {
    if (-not (Test-CommandExists $cmd)) {
        Write-Error "$cmd is not installed or not in PATH. Please install it and try again."
        exit 1
    }
}

# Check Python version
$pythonVersion = (python --version) -replace '^Python (\d+\.\d+).*$', '$1'
if ([version]$pythonVersion -lt [version]"3.8") {
    Write-Error "Python 3.8 or higher is required. Found: $pythonVersion"
    exit 1
}

# Set up virtual environment
$venvPath = "$PSScriptRoot\.venv"
$activateScript = "$venvPath\Scripts\Activate.ps1"

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
