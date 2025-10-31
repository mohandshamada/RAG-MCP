#!/bin/bash
# Docker Operations Script for PDF RAG MCP Server
# Simplifies common Docker and Docker Compose tasks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CONTAINER_NAME="rag-mcp-server"
IMAGE_NAME="pdf-rag-mcp"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

show_help() {
    cat << 'EOF'
PDF RAG MCP Server - Docker Operations

Usage: ./docker_ops.sh [command] [options]

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
  ./docker_ops.sh build              # Build the image
  ./docker_ops.sh up                 # Start the container
  ./docker_ops.sh logs               # View logs
  ./docker_ops.sh shell              # Open shell
  ./docker_ops.sh backup             # Backup data
  ./docker_ops.sh clean              # Clean everything

EOF
}

# Build image
build_image() {
    print_header "Building Docker Image"
    cd "$PROJECT_DIR"
    docker-compose build --no-cache
    print_success "Image built successfully"
}

# Start container
start_container() {
    print_header "Starting Container"
    cd "$PROJECT_DIR"
    docker-compose up -d
    print_success "Container started"
    print_info "Use './docker_ops.sh logs' to view logs"
    sleep 2
    docker-compose ps
}

# Stop container
stop_container() {
    print_header "Stopping Container"
    cd "$PROJECT_DIR"
    docker-compose down
    print_success "Container stopped"
}

# Restart container
restart_container() {
    print_header "Restarting Container"
    cd "$PROJECT_DIR"
    docker-compose restart
    print_success "Container restarted"
}

# View logs
view_logs() {
    print_header "Container Logs (Press Ctrl+C to exit)"
    cd "$PROJECT_DIR"
    docker-compose logs -f "$CONTAINER_NAME"
}

# Check status
check_status() {
    print_header "Container Status"
    cd "$PROJECT_DIR"
    docker-compose ps
    
    # Additional health info
    echo ""
    print_info "Checking container health..."
    if docker-compose ps "$CONTAINER_NAME" | grep -q "Up"; then
        print_success "Container is running"
        docker-compose exec "$CONTAINER_NAME" python -c "from src.rag_server import mcp; print('✓ MCP module loaded successfully')" 2>/dev/null && \
            print_success "MCP server is healthy" || \
            print_error "MCP server health check failed"
    else
        print_error "Container is not running"
    fi
}

# Open shell
open_shell() {
    print_header "Opening Interactive Shell"
    print_info "Type 'exit' to close shell"
    cd "$PROJECT_DIR"
    docker-compose exec "$CONTAINER_NAME" /bin/bash
}

# Clean resources
clean_resources() {
    print_header "Cleaning Docker Resources"
    print_info "This will remove container and volumes"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        cd "$PROJECT_DIR"
        docker-compose down -v
        print_success "Resources cleaned"
    else
        print_info "Clean cancelled"
    fi
}

# Backup data
backup_data() {
    print_header "Backing Up Data"
    BACKUP_FILE="${PROJECT_DIR}/backups/rag_data_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    mkdir -p "${PROJECT_DIR}/backups"
    
    print_info "Creating backup: $BACKUP_FILE"
    docker run --rm \
        -v rag_rag_data:/data \
        -v "${PROJECT_DIR}/backups:/backup" \
        alpine tar czf "/backup/$(basename $BACKUP_FILE)" -C /data . 2>/dev/null
    
    print_success "Backup created: $BACKUP_FILE"
}

# Restore data
restore_data() {
    if [ -z "$1" ]; then
        print_error "Usage: ./docker_ops.sh restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$1" ]; then
        print_error "Backup file not found: $1"
        exit 1
    fi
    
    print_header "Restoring Data"
    read -p "This will overwrite existing data. Continue? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        print_info "Restoring from: $1"
        docker run --rm \
            -v rag_rag_data:/data \
            -v "$(cd "$(dirname "$1")" && pwd):/backup" \
            alpine tar xzf "/backup/$(basename $1)" -C /data
        print_success "Data restored successfully"
    else
        print_info "Restore cancelled"
    fi
}

# Test health
test_health() {
    print_header "Running Health Check"
    cd "$PROJECT_DIR"
    
    if ! docker-compose ps "$CONTAINER_NAME" | grep -q "Up"; then
        print_error "Container is not running"
        exit 1
    fi
    
    print_info "Testing Python environment..."
    docker-compose exec "$CONTAINER_NAME" python -c "
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
"
    
    print_success "Health check completed"
}

# Monitor resources
monitor_resources() {
    print_header "Monitoring Container Resources (Press Ctrl+C to exit)"
    docker stats "$CONTAINER_NAME" --no-stream=false
}

# Main script logic
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    case "$1" in
        build)
            build_image
            ;;
        up)
            build_image
            start_container
            ;;
        down)
            stop_container
            ;;
        restart)
            restart_container
            ;;
        logs)
            view_logs
            ;;
        status)
            check_status
            ;;
        shell)
            open_shell
            ;;
        clean)
            clean_resources
            ;;
        backup)
            backup_data
            ;;
        restore)
            restore_data "$2"
            ;;
        test)
            test_health
            ;;
        monitor)
            monitor_resources
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
