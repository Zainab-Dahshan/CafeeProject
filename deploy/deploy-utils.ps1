<#
.SYNOPSIS
    Deployment utility functions for the Café Application
#>

function Test-CommandExists {
    <#
    .SYNOPSIS
        Tests if a command exists.
    .DESCRIPTION
        Checks if the specified command is available in the current session.
    .PARAMETER Command
        The command to test.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Command
    )
    
    $exists = $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
    return $exists
}

function Invoke-EnsureDirectory {
    <#
    .SYNOPSIS
        Ensures that a directory exists.
    .DESCRIPTION
        Creates the specified directory if it does not exist.
    .PARAMETER Path
        The path to the directory.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Path
    )
    
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created directory: $Path" -ForegroundColor Green
    }
}

function Invoke-EnsureFile {
    <#
    .SYNOPSIS
        Ensures that a file exists.
    .DESCRIPTION
        Creates an empty file if it does not exist.
    .PARAMETER Path
        The path to the file.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Path
    )
    
    if (-not (Test-Path $Path)) {
        New-Item -ItemType File -Path $Path | Out-Null
        Write-Host "Created file: $Path" -ForegroundColor Green
    }
}

function Invoke-EnsureEnvironment {
    <#
    .SYNOPSIS
        Ensures that required environment variables are set.
    .DESCRIPTION
        Checks for required environment variables and prompts for missing ones.
    .PARAMETER Environment
        The deployment environment.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$Environment
    )
    
    $requiredVars = @('FLASK_APP')
    $missingVars = @()
    
    foreach ($var in $requiredVars) {
        if (-not (Test-Path "env:$var")) {
            $missingVars += $var
        }
    }
    
    if ($missingVars.Count -gt 0) {
        Write-Host "The following required environment variables are not set:" -ForegroundColor Yellow
        $missingVars | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
        
        $proceed = Read-Host "Do you want to set them now? (y/n)"
        if ($proceed -eq 'y') {
            foreach ($var in $missingVars) {
                $value = Read-Host "Enter value for $var"
                [Environment]::SetEnvironmentVariable($var, $value, 'Process')
            }
        } else {
            Write-Error "Deployment aborted due to missing environment variables."
            exit 1
        }
    }
}

export-modulemember -function Test-CommandExists, Invoke-EnsureDirectory, Invoke-EnsureFile, Invoke-EnsureEnvironment
