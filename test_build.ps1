# Test Docker Build
# Run this after fixes to verify the build works

Write-Host "Testing Docker Build for PDF RAG MCP Server" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Get the project directory
$projectDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Write-Host "Project directory: $projectDir" -ForegroundColor Yellow

# Change to project directory
Push-Location $projectDir

# Run the build
Write-Host ""
Write-Host "Building Docker image..." -ForegroundColor Green
Write-Host "This may take 2-3 minutes on first build..." -ForegroundColor Yellow
Write-Host ""

docker-compose build --no-cache

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Start the container:"
    Write-Host "     docker-compose up -d" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  2. Check status:"
    Write-Host "     docker-compose ps" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  3. View logs:"
    Write-Host "     docker-compose logs -f" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "✗ BUILD FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Cyan
    Write-Host "  1. Check Docker Desktop is running"
    Write-Host "  2. Check error messages above"
    Write-Host "  3. Try: docker system prune -a"
    Write-Host "  4. Try building again"
}

Pop-Location
