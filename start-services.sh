#!/bin/bash
cd ~/podcast-project
source podcast-env/bin/activate
docker-compose up -d
echo "Windmill and Postgres services started. Access Windmill at http://localhost:8000"
