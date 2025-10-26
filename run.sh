#!/bin/bash

arg=$1
PID_FILE="/tmp/ollama_app.pid"

if [[ "$arg" == "run" ]]; then
    if pgrep -f "ollama serve" >/dev/null; then
    else
        ollama serve > /dev/null 2>&1 &
        echo $! > "$PID_FILE"
    fi

elif [[ "$arg" == "exit" ]]; then
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" >/dev/null; then
            kill "$PID" >/dev/null 2>&1
        fi
        rm -f "$PID_FILE"
    fi
fi
