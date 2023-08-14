@echo off

rem Activate the virtual environment

call .\venv\Scripts\activate

rem Change to the backend directory and start the server
cd .\backend\
start cmd /k python main.py
start cmd /k celery -A tasks worker --loglevel=info
start cmd /k celery -A tasks beat --loglevel=info
start cmd /k celery -A tasks flower --port=5555

rem Change to the frontend directory and start the Vue.js app
cd ..\frontend\
start cmd /k npm run serve
