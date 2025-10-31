#!/bin/bash
# Docker Build Test Script for Linux/Mac
# Run this to test if the Docker build works

echo "========================================="
echo "Testing Docker Build - PDF RAG MCP"
echo "========================================="
echo ""

# Check Docker is running
echo "Checking Docker status..."
if ! docker info > /dev/null 2>&1; then
    echo "✗ Docker is not running. Please start Docker Desktop."
    exit 1
fi
echo "✓ Docker is running"
echo ""

# Get project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Project directory: $PROJECT_DIR"
cd "$PROJECT_DIR"

# Run build
echo ""
echo "Building Docker image..."
echo "This may take 2-3 minutes on first build..."
echo ""

docker-compose build --no-cache

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✓ BUILD SUCCESSFUL!"
    echo "========================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Start the container:"
    echo "   docker-compose up -d"
    echo ""
    echo "2. Check status:"
    echo "   docker-compose ps"
    echo ""
    echo "3. View logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "4. Test the application:"
    echo "   docker-compose exec rag-mcp-server python client.py list"
    echo ""
else
    echo ""
    echo "========================================="
    echo "✗ BUILD FAILED"
    echo "========================================="
    echo ""
    echo "Troubleshooting:"
    echo "1. Check Docker Desktop is running"
    echo "2. Check error messages above"
    echo "3. Try: docker system prune -a"
    echo "4. Try building again"
    echo ""
fi
