#!/usr/bin/env bash

set -e

echo "Initializing database"
until python3 database_init.py 
do
  echo "Database not running or can not connect to it"
  sleep 3
done


echo "Run server"
python3 server.py
