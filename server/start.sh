#!/usr/bin/env bash

set -e

echo "start.sh - Initializing database"
until python3 database_init.py 
do
  echo "start.sh - Database not running or can not connect to it. Retrying..."
  sleep 3
done


echo "start.sh - Running the server"
python3 server.py
