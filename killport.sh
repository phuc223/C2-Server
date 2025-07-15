#!/bin/bash

# Default port if not provided
PORT=${1:-8000} # $1 mean the first argument, :-8000 is the default one

# Help message
usage() {
  echo "Usage: killport [PORT]"
  echo "Kills the process using the given TCP port (default: 8000)"
  echo
  echo "Options:"
  echo "  -h, --help     Show this help message"
  exit 1
}

# Handle help flag
if [[ "$PORT" == "-h" || "$PORT" == "--help" ]]; then
  usage
fi

# Determine command prefixes (use sudo if not root)
if [ "$EUID" -ne 0 ]; then
  LSOF_CMD="sudo lsof"
  KILL_CMD="sudo kill -9"
else
  LSOF_CMD="lsof"
  KILL_CMD="kill -9"
fi

# Get PID using the specified port
PID=$($LSOF_CMD -ti tcp:$PORT)

if [ -z "$PID" ]; then
  echo "✅ No process is using port $PORT."
else
  echo "🔍 Process using port $PORT found: PID $PID"
  $KILL_CMD $PID && echo "🗡️  Killed process $PID using port $PORT."
fi

