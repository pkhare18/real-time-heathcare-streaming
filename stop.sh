#!/bin/bash
 
echo "Stopping all services..."
 
pkill -9 -f processor || true
pkill -9 -f producer || true
pkill -9 -f streamlit || true
pkill -9 -f python || true
 
docker-compose down
 
echo "All services stopped"