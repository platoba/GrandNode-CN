#!/bin/bash
# MongoDB backup script for GrandNode-CN
set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CONTAINER="${MONGO_CONTAINER:-grandnode-mongo}"

mkdir -p "$BACKUP_DIR"

echo "[$(date)] Starting MongoDB backup..."

docker exec "$CONTAINER" mongodump \
    --username="${MONGO_ROOT_USER:-admin}" \
    --password="${MONGO_ROOT_PASS:-changeme}" \
    --authenticationDatabase=admin \
    --db=grandnode \
    --archive="/tmp/grandnode_${TIMESTAMP}.gz" \
    --gzip

docker cp "$CONTAINER:/tmp/grandnode_${TIMESTAMP}.gz" "$BACKUP_DIR/"
docker exec "$CONTAINER" rm "/tmp/grandnode_${TIMESTAMP}.gz"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "grandnode_*.gz" -mtime +7 -delete

echo "[$(date)] Backup complete: $BACKUP_DIR/grandnode_${TIMESTAMP}.gz"
