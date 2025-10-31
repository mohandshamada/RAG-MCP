# Install UV and project dependencies (Windows PowerShell)

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  PDF RAG MCP Server - UV Installation" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if UV is installed
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvInstalled) {
    Write-Host "[1/3] Installing UV (fast Python package manager)..." -ForegroundColor Yellow
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host "      UV installed successfully!" -ForegroundColor Green
} else {
    $uvVersion = uv --version
    Write-Host "[1/3] UV already installed ($uvVersion)" -ForegroundColor Green
}

Write-Host ""
Write-Host "[2/3] Creating virtual environment with UV..." -ForegroundColor Yellow
uv venv

Write-Host ""
Write-Host "[3/3] Installing project dependencies with UV..." -ForegroundColor Yellow
uv pip install -e .

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Installation Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the virtual environment:" -ForegroundColor Yellow
Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run the server:" -ForegroundColor Yellow
Write-Host "  uv run python main.py" -ForegroundColor White
Write-Host "  or: uv run python -m src.rag_server" -ForegroundColor White
Write-Host ""
Write-Host "To run the CLI client:" -ForegroundColor Yellow
Write-Host "  uv run python client.py list" -ForegroundColor White
Write-Host ""
Write-Host "To run tests:" -ForegroundColor Yellow
Write-Host "  uv run python run_tests.py" -ForegroundColor White
Write-Host ""
