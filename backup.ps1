<#
.SYNOPSIS
    Backup script for the Café Application
.DESCRIPTION
    This script creates a backup of the database and important files.
    Backups are stored in the 'backups' directory with timestamps.
.PARAMETER maxBackups
    Maximum number of backups to keep. Oldest backups will be deleted.
.EXAMPLE
    .\backup.ps1 -maxBackups 10
#>

param(
    [int]$maxBackups = 10
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Print header
Write-Host "=== Café Application Backup ===" -ForegroundColor Cyan

# Create backups directory if it doesn't exist
$backupDir = ".\backups"
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Host "Created backup directory: $backupDir" -ForegroundColor Yellow
}

# Generate timestamp for backup file
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = "$backupDir\backup_$timestamp.zip"

# Files and directories to backup
$filesToBackup = @(
    "database.db",
    "logs",
    ".env"
)

# Create backup
Write-Host "Creating backup: $backupFile" -ForegroundColor Yellow
try {
    Compress-Archive -Path $filesToBackup -DestinationPath $backupFile -Force
    Write-Host "Backup created successfully" -ForegroundColor Green
    
    # List all backups, sort by creation time (newest first)
    $backups = Get-ChildItem -Path "$backupDir\backup_*.zip" | Sort-Object CreationTime -Descending
    
    # Remove old backups if we have more than maxBackups
    if ($backups.Count -gt $maxBackups) {
        $backupsToDelete = $backups | Select-Object -Skip $maxBackups
        foreach ($oldBackup in $backupsToDelete) {
            Write-Host "Removing old backup: $($oldBackup.Name)" -ForegroundColor Yellow
            Remove-Item -Path $oldBackup.FullName -Force
        }
    }
    
    # Display backup summary
    Write-Host "`n=== Backup Summary ===" -ForegroundColor Cyan
    Write-Host "Latest backup: $backupFile" -ForegroundColor Green
    Write-Host "Total backups kept: $($backups.Count)" -ForegroundColor Green
    
} catch {
    Write-Error "Failed to create backup: $_"
    exit 1
}

Write-Host "Backup process completed!" -ForegroundColor Green
