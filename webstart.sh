#!/bin/bash

# Start Gunicorn in the background
gunicorn app:app &

# Wait for port 8000 to be available
while ! nc -z localhost 8000; do   
  sleep 0.1 # wait for 1/10 of the second before checking again
done

# Run the second command
python -m RajniiRobot
