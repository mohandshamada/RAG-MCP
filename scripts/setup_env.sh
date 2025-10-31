#!/bin/bash
# PDF RAG MCP Server - UV Setup Script for macOS/Linux
# Run this script to set up the project with UV

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo "$(printf '=%.0s' {1..70})"
    echo -e "${GREEN}🚀 $1${NC}"
    echo "$(printf '=%.0s' {1..70})"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Main Setup
print_header "PDF RAG MCP Server - UV Setup for $(uname)"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="$PROJECT_DIR/.venv"

# Step 1: Check UV Installation
print_header "Step 1: Checking UV Installation"

if command -v uv &> /dev/null; then
    UV_VERSION=$(uv --version)
    print_success "UV is installed: $UV_VERSION"
else
    print_warning "UV not found. Installing UV..."
    print_info "Installing UV from https://astral.sh/uv/install.sh"
    
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add UV to PATH
    export PATH="$HOME/.cargo/bin:$PATH"
    
    print_success "UV installed successfully!"
    print_warning "Please add this to your shell profile (~/.bashrc, ~/.zshrc, etc):"
    echo "export PATH=\"\$HOME/.cargo/bin:\$PATH\""
fi

# Step 2: Create Virtual Environment
print_header "Step 2: Creating Virtual Environment"

if [ -d "$VENV_PATH" ]; then
    print_success "Virtual environment already exists: $VENV_PATH"
else
    print_info "Creating virtual environment..."
    cd "$PROJECT_DIR"
    uv venv
    print_success "Virtual environment created"
fi

# Step 3: Activate Virtual Environment
print_header "Step 3: Activating Environment"

ACTIVATE_SCRIPT="$VENV_PATH/bin/activate"
if [ -f "$ACTIVATE_SCRIPT" ]; then
    source "$ACTIVATE_SCRIPT"
    print_success "Virtual environment activated"
else
    print_error "Could not find activation script"
    exit 1
fi

# Step 4: Install Dependencies
print_header "Step 4: Installing Dependencies"

cd "$PROJECT_DIR"

# Check for dev flag
if [ "$1" == "--dev" ] || [ "$1" == "-d" ]; then
    print_info "Installing with development dependencies..."
    uv pip install -e ".[dev]"
else
    print_info "Installing production dependencies..."
    uv pip install -e "."
fi

print_success "Dependencies installed"

# Step 5: Generate Lock File
print_header "Step 5: Generating Lock File"

print_info "Creating uv.lock file..."
if uv lock; then
    print_success "Lock file generated"
else
    print_warning "Could not generate lock file (non-critical)"
fi

# Step 6: Create Directories
print_header "Step 6: Creating Data Directories"

DIRS=(
    "data/vector_stores"
    "data/document_cache"
    "data/metadata"
    "logs"
)

for dir in "${DIRS[@]}"; do
    DIR_PATH="$PROJECT_DIR/$dir"
    mkdir -p "$DIR_PATH"
    print_success "Created: $DIR_PATH"
done

# Step 7: Verify Installation
print_header "Step 7: Verifying Installation"

if uv pip list | grep -q "pdf-rag-mcp-server"; then
    print_success "Project installed successfully!"
else
    print_warning "Could not verify project installation"
fi

# Print Next Steps
print_header "Setup Complete! 🎉"

echo -e "${BLUE}📋 Next Steps:${NC}"
echo "$(printf '-%.0s' {1..70})"
echo "1. The virtual environment is activated. To deactivate, run:"
echo -e "   ${BLUE}deactivate${NC}"
echo ""
echo "2. Run the server:"
echo -e "   ${BLUE}uv run python src/rag_server.py${NC}"
echo ""
echo "3. In another terminal, test with client:"
echo -e "   ${BLUE}uv run python client.py --help${NC}"
echo ""
echo "4. Configure Claude Desktop:"
echo -e "   ${BLUE}See CLAUDE_DESKTOP_SETUP.md for details${NC}"

echo ""
echo -e "${BLUE}📚 Useful UV Commands:${NC}"
echo "$(printf '-%.0s' {1..70})"
echo -e "  ${BLUE}uv pip list              ${NC}- List installed packages"
echo -e "  ${BLUE}uv lock --upgrade        ${NC}- Update dependencies"
echo -e "  ${BLUE}uv run pytest            ${NC}- Run tests"
echo -e "  ${BLUE}uv run black .           ${NC}- Format code"
echo -e "  ${BLUE}uv run ruff check .      ${NC}- Lint code"

echo ""
echo -e "${BLUE}📖 Documentation:${NC}"
echo "$(printf '-%.0s' {1..70})"
echo -e "  ${BLUE}README.md                ${NC}- Quick start guide"
echo -e "  ${BLUE}UV_INTEGRATION.md        ${NC}- Detailed UV guide"
echo -e "  ${BLUE}CONFIG.md                ${NC}- Configuration reference"

echo ""
echo "$(printf '=%.0s' {1..70})"
print_success "Ready to start! Happy coding! 🚀"
echo "$(printf '=%.0s' {1..70})"
echo ""
