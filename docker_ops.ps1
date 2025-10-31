# Docker Operations Script for PDF RAG MCP Server (PowerShell)
# Simplifies common Docker and Docker Compose tasks on Windows

param(
    [Parameter(Position=0)]
    [string]$Command = "",
    
    [Parameter(Position=1)]
    [string]$Argument = ""
)

# Configuration
$CONTAINER_NAME = "rag-mcp-server"
$IMAGE_NAME = "pdf-rag-mcp"
$PROJECT_DIR = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Color functions
function Print-Header {
    param([string]$Message)
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host $Message -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Blue
}

function Print-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Print-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Yellow
}

function Show-Help {
    $helpText = @"
PDF RAG MCP Server - Docker Operations (PowerShell)

Usage: .\docker_ops.ps1 [command] [options]

Commands:
  build              Build the Docker image
  up                 Start the container (background)
  down               Stop and remove the container
  restart            Restart the container
  logs               View container logs (tail -f)
  status             Check container status
  shell              Open interactive shell in container
  clean              Remove container and volumes
  backup             Backup data volume
  restore FILE       Restore data from backup
  test               Run health check
  monitor            Monitor container resource usage
  help               Show this help message

Examples:
  .\docker_ops.ps1 build              # Build the image
  .\docker_ops.ps1 up                 # Start the container
  .\docker_ops.ps1 logs               # View logs
  .\docker_ops.ps1 shell              # Open shell
  .\docker_ops.ps1 backup             # Backup data
  .\docker_ops.ps1 clean              # Clean everything
"@
    Write-Host $helpText
}

function Build-Image {
    Print-Header "Building Docker Image"
    Push-Location $PROJECT_DIR
    & docker-compose build --no-cache
    Pop-Location
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Image built successfully"
    } else {
        Print-Error "Image build failed"
        exit 1
    }
}

function Start-Container {
    Print-Header "Starting Container"
    Push-Location $PROJECT_DIR
    & docker-compose up -d
    Pop-Location
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Container started"
        Print-Info "Use '.\docker_ops.ps1 logs' to view logs"
        Start-Sleep -Seconds 2
        & docker-compose ps
    } else {
        Print-Error "Failed to start container"
        exit 1
    }
}

function Stop-Container {
    Print-Header "Stopping Container"
    Push-Location $PROJECT_DIR
    & docker-compose down
    Pop-Location
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Container stopped"
    } else {
        Print-Error "Failed to stop container"
        exit 1
    }
}

function Restart-Container {
    Print-Header "Restarting Container"
    Push-Location $PROJECT_DIR
    & docker-compose restart
    Pop-Location
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Container restarted"
    } else {
        Print-Error "Failed to restart container"
        exit 1
    }
}

function View-Logs {
    Print-Header "Container Logs (Press Ctrl+C to exit)"
    Push-Location $PROJECT_DIR
    & docker-compose logs -f $CONTAINER_NAME
    Pop-Location
}

function Check-Status {
    Print-Header "Container Status"
    Push-Location $PROJECT_DIR
    & docker-compose ps
    
    Write-Host ""
    Print-Info "Checking container health..."
    
    $status = & docker-compose ps $CONTAINER_NAME 2>$null | Select-String "Up"
    if ($status) {
        Print-Success "Container is running"
        try {
            & docker-compose exec $CONTAINER_NAME python -c "from src.rag_server import mcp; print('✓ MCP module loaded successfully')" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Print-Success "MCP server is healthy"
            } else {
                Print-Error "MCP server health check failed"
            }
        } catch {
            Print-Error "Could not verify MCP server"
        }
    } else {
        Print-Error "Container is not running"
    }
    
    Pop-Location
}

function Open-Shell {
    Print-Header "Opening Interactive Shell"
    Print-Info "Type 'exit' to close shell"
    Push-Location $PROJECT_DIR
    & docker-compose exec $CONTAINER_NAME cmd /c "powershell"
    Pop-Location
}

function Clean-Resources {
    Print-Header "Cleaning Docker Resources"
    Print-Info "This will remove container and volumes"
    
    $confirm = Read-Host "Are you sure? (yes/no)"
    
    if ($confirm -eq "yes") {
        Push-Location $PROJECT_DIR
        & docker-compose down -v
        Pop-Location
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Resources cleaned"
        } else {
            Print-Error "Failed to clean resources"
            exit 1
        }
    } else {
        Print-Info "Clean cancelled"
    }
}

function Backup-Data {
    Print-Header "Backing Up Data"
    
    $backupDir = Join-Path $PROJECT_DIR "backups"
    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    }
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = Join-Path $backupDir "rag_data_backup_$timestamp.tar.gz"
    
    Print-Info "Creating backup: $backupFile"
    
    & docker run --rm `
        -v rag_rag_data:/data `
        -v "${backupDir}:/backup" `
        alpine tar czf "/backup/rag_data_backup_$timestamp.tar.gz" -C /data .
    
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Backup created: $backupFile"
    } else {
        Print-Error "Backup failed"
        exit 1
    }
}

function Restore-Data {
    param([string]$BackupFile)
    
    if ([string]::IsNullOrEmpty($BackupFile)) {
        Print-Error "Usage: .\docker_ops.ps1 restore <backup_file>"
        exit 1
    }
    
    if (-not (Test-Path $BackupFile)) {
        Print-Error "Backup file not found: $BackupFile"
        exit 1
    }
    
    Print-Header "Restoring Data"
    $confirm = Read-Host "This will overwrite existing data. Continue? (yes/no)"
    
    if ($confirm -eq "yes") {
        Print-Info "Restoring from: $BackupFile"
        
        $backupDir = Split-Path -Parent -Path $BackupFile
        $backupName = Split-Path -Leaf -Path $BackupFile
        
        & docker run --rm `
            -v rag_rag_data:/data `
            -v "$backupDir`:/backup" `
            alpine tar xzf "/backup/$backupName" -C /data
        
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Data restored successfully"
        } else {
            Print-Error "Restore failed"
            exit 1
        }
    } else {
        Print-Info "Restore cancelled"
    }
}

function Test-Health {
    Print-Header "Running Health Check"
    
    Push-Location $PROJECT_DIR
    
    $status = & docker-compose ps $CONTAINER_NAME 2>$null | Select-String "Up"
    if (-not $status) {
        Print-Error "Container is not running"
        Pop-Location
        exit 1
    }
    
    Print-Info "Testing Python environment..."
    
    $healthScript = @"
import sys
from pathlib import Path

print('✓ Python version:', sys.version.split()[0])

try:
    from src.rag_server import mcp
    print('✓ MCP module loaded')
except Exception as e:
    print('✗ MCP module failed:', e)
    sys.exit(1)

try:
    from src.comparison_engine import ComparisonEngine
    print('✓ Comparison engine loaded')
except Exception as e:
    print('✗ Comparison engine failed:', e)
    sys.exit(1)

print('✓ All health checks passed')
"@
    
    & docker-compose exec $CONTAINER_NAME python -c $healthScript
    
    if ($LASTEXITCODE -eq 0) {
        Print-Success "Health check completed"
    } else {
        Print-Error "Health check failed"
        exit 1
    }
    
    Pop-Location
}

function Monitor-Resources {
    Print-Header "Monitoring Container Resources (Press Ctrl+C to exit)"
    & docker stats $CONTAINER_NAME
}

# Main logic
switch ($Command.ToLower()) {
    "build" {
        Build-Image
    }
    "up" {
        Build-Image
        Start-Container
    }
    "down" {
        Stop-Container
    }
    "restart" {
        Restart-Container
    }
    "logs" {
        View-Logs
    }
    "status" {
        Check-Status
    }
    "shell" {
        Open-Shell
    }
    "clean" {
        Clean-Resources
    }
    "backup" {
        Backup-Data
    }
    "restore" {
        Restore-Data $Argument
    }
    "test" {
        Test-Health
    }
    "monitor" {
        Monitor-Resources
    }
    "help" {
        Show-Help
    }
    "" {
        Show-Help
    }
    default {
        Print-Error "Unknown command: $Command"
        Show-Help
        exit 1
    }
}
