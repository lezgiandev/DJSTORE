from yookassa import Configuration, Payment, Payout
from django.conf import settings

Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)


def create_yookassa_payment(amount, payment_token, description):
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Invalid amount value")

    return Payment.create({
        "amount": {
            "value": f"{amount:.2f}",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"{settings.DOMAIN}/api/payment/status/{payment_token}/"
        },
        "capture": True,
        "description": description,
        "metadata": {
            "payment_token": str(payment_token),
            "user_id": str(payment_token)
        }
    })


def create_card_token(card_data):
    response = Configuration.configure(settings.YOOKASSA_SHOP_ID, settings.YOOKASSA_SECRET_KEY)
    return "mock_token_123"


def create_yookassa_payout(amount, fee, card_token):
    return Payout.create({
        "amount": {
            "value": amount - fee,
            "currency": "RUB"
        },
        "payout_destination_data": {
            "type": "bank_card",
            "card": {
                "number": card_token
            }
        },
        "description": "Вывод средств на карту",
        "metadata": {
            "fee": fee
        }
    })
