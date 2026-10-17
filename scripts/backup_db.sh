#!/bin/bash

BACKUP_DIR="$HOME/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/library_db_$DATE.sql"

mkdir -p "$BACKUP_DIR"

docker exec library-db \
  mariadb-dump \
  -u library_app \
  -psecretlibrarypass \
  library_db > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
  echo "Backup created: $BACKUP_FILE"
else
  echo "Backup failed"
  exit 1
fi
