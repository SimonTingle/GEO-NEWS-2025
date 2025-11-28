#!/bin/bash

# Port number we are using for the server
PORT=8080

echo "--- Starting Frontend Server ---"

# 1. CHECK & KILL EXISTING PROCESS ON PORT
# Find the PID listening on the specific port
# lsof -i :8080 checks for processes using that port
# grep LISTEN ensures it's the server listening process
# awk '{print $2}' extracts the PID (Process ID)
PID=$(lsof -t -i :$PORT)

if [ -n "$PID" ]; then
    echo "⚠️  Found existing process (PID: $PID) running on port $PORT."
    kill -9 "$PID"
    echo "✅ Terminated existing process."
else
    echo "✅ Port $PORT is clear."
fi

# 2. START THE SERVER
echo "🚀 Starting Python HTTP server on http://localhost:$PORT"

# The 'exec' command ensures that the server runs in the current shell context
# This is useful, but typically we just run the command directly:
python3 -m http.server $PORT

# Note: Once the server starts, this script will pause here
# until you press Ctrl+C in the terminal.
