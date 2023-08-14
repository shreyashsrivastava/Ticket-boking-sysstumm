#!/bin/bash
start cmd /k sudo service redis-server start

# Activate the virtual environment
source ./venv/bin/activate

# Change to the backend directory and start the server
cd ./backend/
gnome-terminal --tab --title="Flask Server" -- bash -c "python main.py"
gnome-terminal --tab --title="Celery Worker" -- bash -c "celery -A tasks worker --loglevel=info"
gnome-terminal --tab --title="Celery Beat" -- bash -c "celery -A tasks beat --loglevel=info"
gnome-terminal --tab --title="Celery Flower" -- bash -c "celery -A tasks flower --port=5555"

# Change to the frontend directory and start the Vue.js app
cd ../frontend/
gnome-terminal --tab --title="Vue.js App" -- bash -c "npm run serve"
