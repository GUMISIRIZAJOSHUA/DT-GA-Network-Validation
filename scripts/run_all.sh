#!/bin/bash

echo "====================================="
echo "DT-GA NETWORK VALIDATION EXPERIMENT"
echo "====================================="

# Move to project root directory
cd "$(dirname "$0")/.."

echo ""
echo "Starting Digital Twin server..."
python3 code/server.py &

SERVER_PID=$!

sleep 3

echo ""
echo "Starting GA client..."
python3 code/client.py

echo ""
echo "Stopping server..."
kill $SERVER_PID

echo ""
echo "====================================="
echo "Running analysis..."
echo "====================================="

python3 code/analyze.py

echo ""
echo "====================================="
echo "Generating publication figures..."
echo "====================================="

python3 code/publication_figures.py

echo ""
echo "====================================="
echo "Generating publication tables..."
echo "====================================="

python3 code/publication_tables.py

echo ""
echo "====================================="
echo "EXPERIMENT COMPLETE"
echo "====================================="
