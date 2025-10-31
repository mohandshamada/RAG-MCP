# Docker Setup Guide - PDF RAG MCP Server

## Overview

This guide covers deploying your PDF RAG MCP Server using Docker and Docker Compose. The setup includes:

- **Multi-stage Docker build** for optimized image size
- **Docker Compose** orchestration with volume management
- **Health checks** and resource limits
- **Logging configuration** for production use
- **Data persistence** via volumes
- **Optional backup service** for production environments

---

## Quick Start

### Prerequisites

- Docker 20.10+ and Docker Compose 1.29+
- At least 4GB available RAM
- 2GB disk space for base image

### Option 1: Using Docker Compose (Recommended)

```bash
# Navigate to project directory
cd pdf_rag_mcp_server

# Build and start the container
docker-compose up -d

# Check container status
docker-compose ps

# View logs
docker-compose logs -f rag-mcp-server

# Stop the container
docker-compose down
```

### Option 2: Using Docker Directly

```bash
# Build the image
docker build -t pdf-rag-mcp:latest .

# Run the container
docker run -d \
  --name rag-mcp-server \
  -v rag_data:/app/data \
  -v rag_logs:/app/logs \
  -p 8000:8000 \
  --health-cmd='python -c "from src.rag_server import mcp; print(\"healthy\")"' \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  --health-start-period=40s \
  pdf-rag-mcp:latest

# Check status
docker ps
```

---

## Configuration

### Environment Variables

Configure the container using environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1          # Real-time output
  - PYTHONDONTWRITEBYTECODE=1   # Don't create .pyc files
  - DATA_DIR=/app/data          # Data directory path
  - LOG_DIR=/app/logs           # Logs directory path
  - LOG_LEVEL=INFO              # Logging level
```

### Resource Limits

Adjust CPU and memory limits in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '2'                 # Maximum 2 CPUs
      memory: 4G                # Maximum 4GB RAM
    reservations:
      cpus: '1'                 # Reserved 1 CPU
      memory: 2G                # Reserved 2GB RAM
```

### Volumes

The setup uses named volumes for data persistence:

```yaml
volumes:
  rag_data:      # Vector stores, metadata, document cache
    driver: local
  rag_logs:      # Application logs
    driver: local
```

---

## Usage

### Ingesting Documents

```bash
# Interactive mode
docker-compose exec rag-mcp-server python client.py ingest /app/documents/sample.pdf my_document

# Or use the CLI with document mounted
docker run -v $(pwd)/documents:/app/documents \
  pdf-rag-mcp:latest \
  python client.py ingest /app/documents/report.pdf my_doc
```

### Querying Documents

```bash
# Inside container
docker-compose exec rag-mcp-server python client.py query my_document "What is the main topic?"

# List all indexed documents
docker-compose exec rag-mcp-server python client.py list
```

### Running the MCP Server

The container runs the MCP server by default on port 8000:

```bash
# View server logs
docker-compose logs -f rag-mcp-server

# Check if server is healthy
docker-compose ps
```

---

## Advanced Usage

### Mounting Local Documents

To process documents from your local machine:

1. Create a `documents` directory in your project root:
   ```bash
   mkdir documents
   cp /path/to/your/documents/*.pdf documents/
   ```

2. The `docker-compose.yml` already mounts this:
   ```yaml
   volumes:
     - ./documents:/app/documents:ro
   ```

3. Process them inside the container:
   ```bash
   docker-compose exec rag-mcp-server python client.py ingest /app/documents/sample.pdf my_doc
   ```

### Data Persistence

Data is automatically persisted in Docker volumes:

```bash
# View volumes
docker volume ls | grep rag

# Inspect volume
docker volume inspect rag_rag_data

# Backup volume
docker run --rm -v rag_rag_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/rag_data_backup.tar.gz -C /data .
```

### Interactive Development

```bash
# Start container with interactive shell
docker-compose run --rm rag-mcp-server /bin/bash

# Inside container, run commands
python client.py list
python -c "from src.rag_server import mcp; print('MCP available')"
```

### Multi-Container Setup

For production environments with multiple services:

```bash
# Scale to multiple instances (if stateless)
docker-compose up -d --scale rag-mcp-server=3

# View all instances
docker-compose ps
```

---

## Monitoring and Maintenance

### View Logs

```bash
# Real-time logs
docker-compose logs -f rag-mcp-server

# Last 100 lines
docker-compose logs --tail=100 rag-mcp-server

# Logs from specific time
docker-compose logs --since=2025-01-01 rag-mcp-server
```

### Health Checks

```bash
# Check health status
docker-compose ps

# Manual health check
docker-compose exec rag-mcp-server python -c "from src.rag_server import mcp; print('OK')"
```

### Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (WARNING: Deletes all data)
docker-compose down -v

# Remove images
docker rmi pdf-rag-mcp:latest

# Remove all dangling resources
docker system prune -a
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs rag-mcp-server

# Common issue: Port already in use
# Change port in docker-compose.yml:
ports:
  - "8001:8000"  # Use 8001 instead

# Rebuild image
docker-compose build --no-cache
docker-compose up -d
```

### Out of Memory

```bash
# Increase memory limit in docker-compose.yml:
deploy:
  resources:
    limits:
      memory: 8G  # Increase from 4G to 8G

# Restart with new limits
docker-compose down
docker-compose up -d
```

### Permission Denied Errors

```bash
# Ensure proper permissions
docker-compose exec rag-mcp-server chmod -R 755 /app/data /app/logs

# Or run as root during troubleshooting
docker-compose exec -u root rag-mcp-server chown -R nobody:nogroup /app/data
```

### Slow Performance

```bash
# Check resource usage
docker stats rag-mcp-server

# If CPU/Memory maxed out, increase limits
# Rebuild and restart
docker-compose build --no-cache
docker-compose restart
```

---

## Production Deployment

### Enable Backup Service

Uncomment the `backup-service` in `docker-compose.yml`:

```yaml
backup-service:
  image: busybox:latest
  volumes:
    - rag_data:/data:ro
    - ./backups:/backups
  command: >
    sh -c "
    while true; do
      tar -czf /backups/rag_data_$(date +%Y%m%d_%H%M%S).tar.gz /data;
      find /backups -mtime +7 -delete;
      sleep 86400;
    done
    "
```

### Docker Swarm (Multi-Machine)

```bash
# Initialize Swarm
docker swarm init

# Deploy service
docker stack deploy -c docker-compose.yml rag-mcp

# View services
docker service ls

# View logs
docker service logs rag-mcp_rag-mcp-server
```

### Kubernetes Deployment

For Kubernetes, convert Docker Compose or create manifests:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rag-mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rag-mcp-server
  template:
    metadata:
      labels:
        app: rag-mcp-server
    spec:
      containers:
      - name: rag-mcp-server
        image: pdf-rag-mcp:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: logs
          mountPath: /app/logs
        livenessProbe:
          exec:
            command:
            - python
            - -c
            - from src.rag_server import mcp; print('healthy')
          initialDelaySeconds: 40
          periodSeconds: 30
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: rag-data-pvc
      - name: logs
        persistentVolumeClaim:
          claimName: rag-logs-pvc
```

---

## Performance Tips

1. **Use SSD storage** for vector store volumes
2. **Allocate adequate memory** - at least 2GB reserved
3. **CPU cores** - 2+ cores recommended for embedding generation
4. **Network** - Keep Docker daemon and volumes on same machine
5. **Logging** - Rotate logs regularly to prevent disk overflow

---

## Security Best Practices

1. **Don't run as root** - Dockerfile uses default unprivileged user
2. **Scan image** - `docker scan pdf-rag-mcp:latest`
3. **Use secrets** - Don't hardcode API keys in environment
4. **Read-only volumes** where possible - `./documents:/app/documents:ro`
5. **Network isolation** - Use named networks, avoid `--network host`
6. **Image signing** - Sign and verify production images

---

## Support & Issues

For detailed logs:
```bash
docker-compose logs --tail=200 rag-mcp-server
```

For rebuild from scratch:
```bash
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

Check the main README.md for usage examples and additional information.
