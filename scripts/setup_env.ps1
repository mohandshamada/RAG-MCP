# PDF RAG MCP Server - UV Setup Script for Windows (PowerShell)
# Run this script to set up the project with UV

param(
    [switch]$Dev = $false,
    [switch]$SkipUV = $false
)

$ErrorActionPreference = "Stop"

function Write-Header {
    param([string]$Text)
    Write-Host "`n$('='*70)" -ForegroundColor Cyan
    Write-Host "🚀 $Text" -ForegroundColor Green
    Write-Host "$('='*70)`n" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✅ $Text" -ForegroundColor Green
}

function Write-Error {
    param([string]$Text)
    Write-Host "❌ $Text" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠️  $Text" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Text)
    Write-Host "ℹ️  $Text" -ForegroundColor Blue
}

# Main Setup
Write-Header "PDF RAG MCP Server - UV Setup for Windows"

# Step 1: Check UV Installation
if (-not $SkipUV) {
    Write-Header "Step 1: Checking UV Installation"
    
    try {
        $version = & uv --version 2>$null
        Write-Success "UV is installed: $version"
    }
    catch {
        Write-Warning "UV not found. Installing UV..."
        Write-Info "Installing UV from https://astral.sh/uv/install.ps1"
        
        Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -OutFile $env:TEMP\uv_install.ps1
        & powershell -ExecutionPolicy ByPass -File $env:TEMP\uv_install.ps1
        
        # Add UV to PATH
        $uvPath = "$env:USERPROFILE\.cargo\bin"
        if ($uvPath -notin $env:PATH.Split(';')) {
            $env:PATH += ";$uvPath"
            [Environment]::SetEnvironmentVariable("PATH", $env:PATH, [EnvironmentVariableTarget]::User)
        }
        
        Write-Success "UV installed successfully!"
        Write-Warning "Please restart PowerShell to use UV"
    }
}

# Step 2: Create Virtual Environment
Write-Header "Step 2: Creating Virtual Environment"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $projectDir ".venv"

if (Test-Path $venvPath) {
    Write-Success "Virtual environment already exists: $venvPath"
}
else {
    Write-Info "Creating virtual environment..."
    & uv venv
    Write-Success "Virtual environment created"
}

# Step 3: Activate Virtual Environment
Write-Header "Step 3: Setting Up Environment"

$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    & $activateScript
    Write-Success "Virtual environment activated"
}
else {
    Write-Error "Could not find activation script"
    exit 1
}

# Step 4: Install Dependencies
Write-Header "Step 4: Installing Dependencies"

if ($Dev) {
    Write-Info "Installing with development dependencies..."
    & uv pip install -e ".[dev]"
}
else {
    Write-Info "Installing production dependencies..."
    & uv pip install -e "."
}

Write-Success "Dependencies installed"

# Step 5: Generate Lock File
Write-Header "Step 5: Generating Lock File"

Write-Info "Creating uv.lock file..."
try {
    & uv lock
    Write-Success "Lock file generated"
}
catch {
    Write-Warning "Could not generate lock file (non-critical)"
}

# Step 6: Create Directories
Write-Header "Step 6: Creating Data Directories"

$dirs = @(
    "data\vector_stores",
    "data\document_cache",
    "data\metadata",
    "logs"
)

foreach ($dir in $dirs) {
    $dirPath = Join-Path $projectDir $dir
    New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    Write-Success "Created: $dirPath"
}

# Step 7: Verify Installation
Write-Header "Step 7: Verifying Installation"

$packages = & uv pip list
if ($packages -match "pdf-rag-mcp-server") {
    Write-Success "Project installed successfully!"
}
else {
    Write-Warning "Could not verify project installation"
}

# Print Next Steps
Write-Header "Setup Complete! 🎉"

Write-Info "📋 Next Steps:"
Write-Host "-" * 70
Write-Host "1. Activate virtual environment (if not already active):"
Write-Host "   $activateScript" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Run the server:"
Write-Host "   uv run python src/rag_server.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. In another terminal, test with client:"
Write-Host "   uv run python client.py --help" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Configure Claude Desktop:"
Write-Host "   See CLAUDE_DESKTOP_SETUP.md for details" -ForegroundColor Cyan

Write-Info "📚 Useful UV Commands:"
Write-Host "-" * 70
Write-Host "  uv pip list              - List installed packages" -ForegroundColor Gray
Write-Host "  uv lock --upgrade        - Update dependencies" -ForegroundColor Gray
Write-Host "  uv run pytest            - Run tests" -ForegroundColor Gray
Write-Host "  uv run black .           - Format code" -ForegroundColor Gray
Write-Host "  uv run ruff check .      - Lint code" -ForegroundColor Gray

Write-Info "📖 Documentation:"
Write-Host "-" * 70
Write-Host "  README.md                - Quick start guide" -ForegroundColor Gray
Write-Host "  UV_INTEGRATION.md        - Detailed UV guide" -ForegroundColor Gray
Write-Host "  CONFIG.md                - Configuration reference" -ForegroundColor Gray

Write-Host "`n$('='*70)" -ForegroundColor Cyan
Write-Success "Ready to start! Happy coding! 🚀"
Write-Host "$('='*70)`n" -ForegroundColor Cyan
