@echo off
echo Запуск проекта...

REM Запуск бэкенда
start cmd /k "cd server && (if exist .venv\Scripts\activate.bat (.venv\Scripts\activate.bat && echo Активация существующего окружения...) else (echo Создание нового окружения... && python -m venv .venv && .venv\Scripts\activate.bat && pip install -r requirements.txt && python manage.py migrate)) && python manage.py runserver"

REM Ждем 5 секунд для запуска бэкенда
timeout /t 5

REM Запуск фронтенда
start cmd /k "cd client && npm install && npm run dev"

echo Проект запущен!
echo Бэкенд доступен по адресу: http://localhost:8000/
echo Фронтенд доступен по адресу: http://localhost:5173/ 