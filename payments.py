import uuid
from typing import Dict


def create_payment(user_id: int, amount: int):
    return {
        "payment_id": f"test_{user_id}",
        "amount": amount,
        "confirmation_url": "https://yookassa.ru/test-payment"
    }


def check_payment(payment_id: str) -> bool:

    return True