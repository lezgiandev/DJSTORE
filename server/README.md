# DJ Site API Documentation

## Base URL
```
http://127.0.0.1:8000/api/
```

## Authentication
API использует JWT (JSON Web Token) для аутентификации. Для получения токена используйте эндпоинт `/token/`.

### Получение токена
```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Ответ:
```json
{
    "access": "your_access_token",
    "refresh": "your_refresh_token"
}
```

Для авторизованных запросов добавьте заголовок:
```
Authorization: Bearer your_access_token
```

## API Endpoints

### Регистрация заведения
```http
POST /api/register/
Content-Type: application/json

{
    "username": "venue_username",
    "password": "venue_password",
    "email": "venue@example.com",
    "name": "Venue Name",
    "city": "City Name",
    "phone": "+1234567890"
}
```

Все поля являются обязательными:
- `username` - уникальное имя пользователя
- `password` - пароль
- `email` - email адрес
- `name` - название заведения
- `city` - город
- `phone` - номер телефона в формате +7XXXXXXXXXX

### Профиль заведения
```http
GET /api/profile/
Authorization: Bearer your_access_token
```

Ответ:
```json
{
    "id": 1,
    "name": "Venue Name",
    "city": "City Name",
    "phone": "+1234567890",
    "qr_code": "/media/qr_codes/qr_1.png",
    "balance": 1000
}
```

+ ### Редактирование профиля заведения
+ ```http
+ PATCH /api/profile/
+ Authorization: Bearer your_access_token
+ Content-Type: application/json
+
+ {
+     "name": "Updated Venue Name",
+     "city": "New City",
+     "phone": "+71234567890"
+ }
+ ```
+ 
+ Поля `qr_code` и `balance` являются только для чтения и не могут быть изменены через API.

### Список треков заведения
```http
GET /api/venue/{venue_id}/tracks/
```

Параметры запроса:
- `genre` - фильтр по жанру
- `search` - поиск по названию или исполнителю

Ответ:
```json
[
    {
        "id": 1,
        "title": "Track Title",
        "genre": {
            "id": 1,
            "name": "Genre Name"
        },
        "artist": "Artist Name",
        "price": 100
    }
]
```

### Добавление трека
```http
POST /api/venue/{venue_id}/tracks/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "title": "Track Title",
    "genre_id": 1,
    "artist": "Artist Name",
    "price": 100
}
```

### Детали трека
```http
GET /api/venue/{venue_id}/tracks/{track_id}/
```

+ ### Редактирование трека
+ ```http
+ PATCH /api/venue/{venue_id}/tracks/{track_id}/
+ Authorization: Bearer your_access_token
+ Content-Type: application/json
+
+ {
+     "title": "Updated Title",
+     "genre_id": 2,
+     "artist": "New Artist",
+     "price": 200
+ }
+ ```

### Удаление трека
```http
DELETE /api/venue/{venue_id}/tracks/{track_id}/
Authorization: Bearer your_access_token
```

### Создание запроса на трек
```http
POST /api/venue/{venue_id}/request/
Content-Type: application/json

{
    "track": 1,
    "user_fee": 400
}
```

Ответ:
```json
{
    "id": 1,
    "payment_url": "http://127.0.0.1:8000/api/requests/pay/{payment_token}/",
    "track": {
        "id": 1,
        "title": "Track Title",
        "genre": {
            "id": 1,
            "name": "Genre Name"
        },
        "artist": "Artist Name",
        "price": 100
    },
    "user_fee": 400,
    "min_fee": 100,
    "status": "pending",
    "is_paid": false,
    "payment_token": "uuid-payment-token",
    "created_at": "2024-05-10T23:43:40Z"
}
```

### Оплата запроса
```http
POST /api/requests/pay/{payment_token}/
Content-Type: application/json

{
    "amount": 400
}
```

### Список запросов
```http
GET /api/requests/
Authorization: Bearer your_access_token
```

Ответ:
```json
[
    {
        "id": 1,
        "payment_url": "http://127.0.0.1:8000/api/requests/pay/{payment_token}/",
        "track": {
            "id": 1,
            "title": "Track Title",
            "genre": {
                "id": 1,
                "name": "Genre Name"
            },
            "artist": "Artist Name",
            "price": 100
        },
        "user_fee": 400,
        "min_fee": 100,
        "status": "pending",
        "is_paid": false,
        "payment_token": "uuid-payment-token",
        "created_at": "2024-05-10T23:43:40Z"
    }
]
```

### Обновление статуса запроса
```http
PATCH /api/requests/{request_id}/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "status": "accepted"
}
```

Возможные статусы:
- `pending` - ожидает
- `accepted` - принят
- `rejected` - отклонен

### Создание заявки на вывод средств
```http
POST /api/withdrawals/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "amount": 1000,
    "card_number": "1234567890123456",
    "card_expiry_year": "2025",
    "card_expiry_month": "12",
    "card_csc": "123"
}
```

### Список жанров
```http
GET /api/genres/
Authorization: Bearer your_access_token
```

Ответ:
```json
[
    {
        "id": 1,
        "name": "Genre Name"
    }
]
```

### Создание жанра
```http
POST /api/genres/
Authorization: Bearer your_access_token
Content-Type: application/json

{
    "name": "New Genre"
}
```

### Список транзакций
```http
GET /api/transactions/
Authorization: Bearer your_access_token
```

Ответ:
```json
[
    {
        "id": 1,
        "amount": 1000,
        "type": "income",
        "description": "Payment for track request",
        "created_at": "2024-05-10T23:43:40Z"
    }
]
```

### История выводов средств
```http
GET /api/withdrawals/history/
Authorization: Bearer your_access_token
```

Ответ:
```json
[
    {
        "id": 1,
        "amount": 1000,
        "bank_card_token": "token_123",
        "fee": 50,
        "status": "processing",
        "yookassa_payout_id": "payout_123",
        "created_at": "2024-05-10T23:43:40Z"
    }
]
```

### Создание платежа
```http
POST /api/payment/{payment_token}/
Authorization: Bearer your_access_token
```

Ответ:
```json
{
    "confirmation_url": "https://yookassa.ru/payment/confirmation"
}
```

### Webhook для платежей
```http
POST /api/payment-webhook/
Content-Type: application/json

{
    "event": "payment.succeeded",
    "object": {
        "id": "payment_id",
        "status": "succeeded",
        "amount": {
            "value": "1000.00",
            "currency": "RUB"
        }
    }
}
```

### Webhook для выводов средств
```http
POST /api/withdrawal-webhook/
Content-Type: application/json

{
    "event": "payout.succeeded",
    "object": {
        "id": "payout_id",
        "status": "succeeded",
        "amount": {
            "value": "1000.00",
            "currency": "RUB"
        }
    }
}
```

## Коды статусов
- 200: Успешный запрос
- 201: Успешное создание
- 400: Ошибка в запросе
- 401: Не авторизован
- 403: Доступ запрещен
- 404: Ресурс не найден
- 500: Внутренняя ошибка сервера

## Примечания
1. Все суммы указываются в копейках
2. QR-код генерируется автоматически при регистрации заведения
3. Для работы с API необходимо быть авторизованным, кроме публичных эндпоинтов
4. При создании запроса на трек необходимо указать сумму не меньше минимальной цены трека
5. Для оплаты запроса используйте полученный payment_token
6. Статус запроса можно изменить только если он находится в статусе "pending"
7. Запрос можно принять только если он оплачен