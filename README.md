# Веб-приложение на Django и Vue.js

Этот проект представляет собой полнофункциональное веб-приложение, состоящее из:
- Бэкенд: Django/Django REST Framework
- Фронтенд: Vue.js с Tailwind CSS и Pinia

## Системные требования

- Python 3.10 или выше
- Node.js 18 или выше
- npm (устанавливается вместе с Node.js)

## Установка

### 1. Скачивание и установка необходимого ПО

#### Python
1. Перейдите на [официальный сайт Python](https://www.python.org/downloads/)
2. Скачайте и установите Python 3.10 или выше
3. При установке выберите опцию "Add Python to PATH"

#### Node.js
1. Перейдите на [официальный сайт Node.js](https://nodejs.org/)
2. Скачайте и установите Node.js 18 или выше (рекомендуется LTS-версия)

### 2. Скачайте проект с гитхаб

1. Нажмите на зелёную кнопку "<> Code" вверху страницы
2. Нажмите скачать zip
3. Распакуйте проект в удобное место

### 3. Настройка бэкенда (Django)

1. Перейдите в директорию сервера:
```bash
cd server
```

2. Создайте и активируйте виртуальное окружение:

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/MacOS:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Выполните миграции базы данных:
```bash
python manage.py migrate
```

5. Создайте суперпользователя (admin):
```bash
python manage.py createsuperuser
```

### 4. Настройка фронтенда (Vue.js)

1. Перейдите в директорию клиента:
```bash
cd ../client
```

2. Установите зависимости:
```bash
npm install
```

## Запуск проекта

### Автоматический запуск

Для удобства в проекте предусмотрены скрипты автоматического запуска:

#### Windows
Просто запустите файл `start_project.bat`, дважды кликнув по нему в проводнике.

Или через командную строку:
```bash
start_project.bat
```

#### Linux/MacOS
Сделайте скрипт исполняемым и запустите его:
```bash
chmod +x start_project.sh
./start_project.sh
```

Скрипты запустят и бэкенд, и фронтенд одновременно.

### Ручной запуск

#### Запуск бэкенда

1. Перейдите в директорию сервера (если вы еще не там):
```bash
cd server
```

2. Активируйте виртуальное окружение (если оно еще не активировано):

Windows:
```bash
.venv\Scripts\activate
```

Linux/MacOS:
```bash
source .venv/bin/activate
```

3. Запустите сервер разработки:
```bash
python manage.py runserver
```

Бэкенд будет доступен по адресу: http://localhost:8000/

Панель администратора Django: http://localhost:8000/admin/

#### Запуск фронтенда

1. Перейдите в директорию клиента (если вы еще не там):
```bash
cd ../client
```

2. Запустите сервер разработки:
```bash
npm run dev
```

Фронтенд будет доступен по адресу: http://localhost:5173/

## Структура проекта

### Бэкенд
- `server/`: Основная директория Django проекта
- `core/`: Основное приложение Django
- `server/settings.py`: Настройки проекта Django
- `requirements.txt`: Зависимости Python

### Фронтенд
- `client/`: Основная директория Vue.js проекта
- `client/src/`: Исходный код Vue приложения
- `client/src/views/`: Vue компоненты страниц
- `client/src/components/`: Переиспользуемые Vue компоненты
- `client/src/api/`: API клиент для взаимодействия с бэкендом
- `client/src/stores/`: Хранилища состояния Pinia
- `client/public/`: Статические файлы

## Сборка для продакшена

### Сборка фронтенда
```bash
cd client
npm run build
```

Сборка будет создана в директории `client/dist/`.

### Настройка бэкенда для продакшена
```bash
cd server
python manage.py collectstatic
```

