#!/bin/bash
# Install UV and project dependencies (Unix/Linux/macOS)

set -e

echo "========================================="
echo "  PDF RAG MCP Server - UV Installation"
echo "========================================="
echo

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "[1/3] Installing UV (fast Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "      UV installed successfully!"
else
    echo "[1/3] UV already installed ($(uv --version))"
fi

echo
echo "[2/3] Creating virtual environment with UV..."
uv venv

echo
echo "[3/3] Installing project dependencies with UV..."
uv pip install -e .

echo
echo "========================================="
echo "  Installation Complete!"
echo "========================================="
echo
echo "To activate the virtual environment:"
echo "  source .venv/bin/activate"
echo
echo "To run the server:"
echo "  uv run python main.py"
echo "  or: uv run python -m src.rag_server"
echo
echo "To run the CLI client:"
echo "  uv run python client.py list"
echo
echo "To run tests:"
echo "  uv run python run_tests.py"
echo
