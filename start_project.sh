#!/bin/bash
echo "Запуск проекта..."

# Запуск бэкенда в отдельном терминале
cd server || exit
if [ -d ".venv" ]; then
    echo "Активация существующего окружения..."
    source .venv/bin/activate
else
    echo "Создание нового окружения..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py migrate
fi
python manage.py runserver &
backend_pid=$!

# Ждем 5 секунд для запуска бэкенда
sleep 5

# Запуск фронтенда
cd ../client || exit
npm install
npm run dev &
frontend_pid=$!

echo "Проект запущен!"
echo "Бэкенд доступен по адресу: http://localhost:8000/"
echo "Фронтенд доступен по адресу: http://localhost:3000/"
echo "Для остановки нажмите Ctrl+C"

# Обработка сигнала прерывания для корректного завершения
trap "kill $backend_pid $frontend_pid; exit" INT TERM
wait 