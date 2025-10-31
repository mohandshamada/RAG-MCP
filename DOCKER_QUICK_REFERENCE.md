# Docker Quick Reference - PDF RAG MCP Server

## One-Liners

### Quick Start
```bash
# Linux/Mac
docker-compose up -d && docker-compose logs -f

# Windows PowerShell
.\docker_ops.ps1 up
.\docker_ops.ps1 logs
```

### Build Only
```bash
docker-compose build --no-cache
```

### Stop Everything
```bash
docker-compose down
```

---

## Common Tasks

### View Logs
```bash
# Real-time logs
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50

# Only errors
docker-compose logs --tail=100 | grep -i error
```

### Access Container
```bash
# Interactive shell
docker-compose exec rag-mcp-server /bin/bash

# Run single command
docker-compose exec rag-mcp-server python client.py list
```

### Data Management
```bash
# List volumes
docker volume ls | grep rag

# Inspect volume
docker volume inspect rag_rag_data

# Backup data
docker run --rm -v rag_rag_data:/data -v $(pwd)/backups:/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Restore data
docker run --rm -v rag_rag_data:/data -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

---

## Troubleshooting

### Container Not Starting
```bash
# Check logs
docker-compose logs --tail=100

# Rebuild image
docker-compose build --no-cache
docker-compose up -d

# Full reset
docker-compose down -v
docker system prune -a
docker-compose up -d
```

### Out of Memory
```bash
# Check memory usage
docker stats

# Adjust in docker-compose.yml and restart
docker-compose restart
```

### Port Already In Use
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Change port in docker-compose.yml:
# ports:
#   - "8001:8000"

docker-compose restart
```

### Permission Issues
```bash
# Fix data directory permissions
docker-compose exec -u root rag-mcp-server \
  chown -R nobody:nogroup /app/data

# Or run with proper user
docker-compose exec rag-mcp-server chmod -R 755 /app/data
```

---

## Performance Optimization

### Check Resource Usage
```bash
docker stats

# Continuous monitoring (5s updates)
watch -n 5 'docker stats --no-stream'
```

### Increase Limits
Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '4'
      memory: 8G
    reservations:
      cpus: '2'
      memory: 4G
```

### Clean Up Unused Resources
```bash
# Remove stopped containers
docker container prune

# Remove dangling images
docker image prune

# Remove unused volumes
docker volume prune

# Complete cleanup
docker system prune -a
```

---

## Deployment Variations

### Production Single Container
```bash
docker run -d \
  --name rag-mcp-prod \
  -v rag_data:/app/data \
  -v rag_logs:/app/logs \
  -e LOG_LEVEL=WARNING \
  --restart unless-stopped \
  --health-cmd='python -c "from src.rag_server import mcp; print(1)"' \
  --health-interval=60s \
  pdf-rag-mcp:latest
```

### Development Mode
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

### Multiple Instances (Load Balanced)
```bash
# Start 3 instances on different ports
for i in {8001..8003}; do
  docker run -d \
    --name rag-mcp-$i \
    -p $i:8000 \
    -v rag_data:/app/data \
    pdf-rag-mcp:latest
done
```

---

## Useful Docker Commands

### Build & Run
```bash
# Build image
docker build -t pdf-rag-mcp:latest .

# Run container
docker run -d --name rag-mcp -p 8000:8000 pdf-rag-mcp:latest

# Run with volume
docker run -d --name rag-mcp -v rag_data:/app/data pdf-rag-mcp:latest
```

### Container Management
```bash
# List containers
docker ps -a

# Stop container
docker stop rag-mcp

# Remove container
docker rm rag-mcp

# Restart container
docker restart rag-mcp

# Inspect container
docker inspect rag-mcp
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi pdf-rag-mcp:latest

# Tag image
docker tag pdf-rag-mcp:latest pdf-rag-mcp:v1.0.0

# Push to registry
docker push your-registry/pdf-rag-mcp:latest
```

### Network
```bash
# List networks
docker network ls

# Inspect network
docker network inspect bridge

# Create network
docker network create rag-network
```

### Logs & Stats
```bash
# View logs
docker logs -f rag-mcp

# Copy logs to file
docker logs rag-mcp > container.log 2>&1

# Resource stats
docker stats rag-mcp

# Inspect events
docker events --filter container=rag-mcp
```

---

## Docker Compose Cheat Sheet

### Common Commands
```bash
# Build services
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View status
docker-compose ps

# View logs
docker-compose logs -f

# Execute command
docker-compose exec rag-mcp-server bash

# Restart service
docker-compose restart

# Remove volumes
docker-compose down -v

# Force recreate
docker-compose up -d --force-recreate
```

### Useful Options
```bash
# Build without cache
docker-compose build --no-cache

# Stop containers only (keep volumes)
docker-compose stop

# Run one-off command
docker-compose run --rm rag-mcp-server python client.py list

# Scale service
docker-compose up -d --scale rag-mcp-server=3

# Override file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Security Best Practices

### Scan Image for Vulnerabilities
```bash
docker scan pdf-rag-mcp:latest
```

### Run as Non-Root
```yaml
# In docker-compose.yml
rag-mcp-server:
  user: "1000:1000"  # Run as non-root user
```

### Use Secrets (Not Environment Variables)
```bash
# Create secret
echo "my-secret-value" | docker secret create my-secret -

# Use in compose
secrets:
  my-secret:
    external: true
```

### Network Isolation
```bash
# Use custom network (safer than default bridge)
docker network create rag-network
docker-compose --project-name rag up -d
```

---

## Integration Examples

### With Claude Desktop (if applicable)
```bash
# Get container IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' rag-mcp-server

# Connect Claude to MCP server
# Update Claude config with container IP and port
```

### With Other Services
```yaml
# docker-compose.yml with multiple services
version: '3.9'
services:
  rag-mcp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - rag_data:/app/data
  
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - rag-mcp
```

---

## Resources

- Docker Docs: https://docs.docker.com/
- Docker Compose Docs: https://docs.docker.com/compose/
- Best Practices: https://docs.docker.com/develop/dev-best-practices/
- Security: https://docs.docker.com/engine/security/

---

## Quick Scripts

### Auto-Restart Failed Containers
```bash
# Check every minute, restart if needed
while true; do
  docker ps | grep rag-mcp || docker start rag-mcp
  sleep 60
done
```

### Automated Daily Backup
```bash
# Add to crontab: 0 2 * * * /path/to/backup.sh
#!/bin/bash
docker run --rm -v rag_rag_data:/data -v /backups:/backup \
  alpine tar czf /backup/backup_$(date +\%Y\%m\%d).tar.gz -C /data .
```

### Monitor and Alert
```bash
# Simple monitoring
docker stats --no-stream | awk 'NR>1 {if($4>50) print "WARNING: High memory: "$0}'
```
