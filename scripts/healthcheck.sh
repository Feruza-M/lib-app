#!/bin/bash

URL="http://localhost:8000/health"

if curl -fs "$URL" | grep -q '"status":"ok"'; then
    echo "Application is working"
    exit 0
else
    echo "Application is NOT working"
    exit 1
fi
