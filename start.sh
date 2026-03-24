#!/bin/bash
 
echo "Cleaning old processes..."
pkill -9 -f python || true
pkill -9 -f streamlit || true
 
echo "Starting Docker services..."
docker-compose up -d
 
echo "Waiting for Postgres to be ready..."
sleep 5
 
echo "Starting Processor..."
nohup python processor/processor.py > processor.log 2>&1 &
 
echo "Starting Producer..."
nohup python producer/producer.py > producer.log 2>&1 &
 
echo "Starting Streamlit..."
nohup streamlit run streamlit_app/app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
 
echo "All services started!"
echo "Open Streamlit on port 8501"