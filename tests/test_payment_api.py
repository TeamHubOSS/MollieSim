import time
import requests
import datetime

from deepdiff import DeepDiff
from freezegun import freeze_time

from .utils import MollieTestCase


class TestPaymentApi(MollieTestCase):
    def test_create_payment(self):
        payload = {
            "amount": {"currency": "EUR", "value": "100.00"},
            "description": "My first API payment",
            "webhookUrl": "https://webshop.example.org/mollie-webhook/",
            "redirectUrl": "https://webshop.example.org/order/12345/",
        }
        rv = requests.post("http://localhost:3333/v2/payments", json=payload)
        self.assertEqual(rv.status_code, 201, msg=rv.json())

    @freeze_time("2022-06-01")
    def test_list_payments(self):
        payload = {
            "amount": {"currency": "EUR", "value": "100.00"},
            "description": "My first API payment",
            "webhookUrl": "https://webshop.example.org/mollie-webhook/",
            "redirectUrl": "https://webshop.example.org/order/12345/",
        }
        rv = requests.post("http://localhost:3333/v2/payments", json=payload)
        self.assertEqual(rv.status_code, 201, msg=rv.json())

        rv = requests.get("http://localhost:3333/v2/payments", json=payload)
        self.assertEqual(rv.status_code, 200, msg=rv.json())

        expected = {
            "_embed": {
                "payments": [
                    {
                        "resource": "payment",
                        "amount": {"currency": "EUR", "value": "100.00"},
                        "description": "My first API payment",
                        "webhookUrl": "https://webshop.example.org/mollie-webhook/",
                        "redirectUrl": "https://webshop.example.org/order/12345/",
                        "sequenceType": "oneoff",
                        "createdAt": "2022-06-01T00:00:00",
                        "metadata": None,
                        "status": "open",
                    },
                ]
            },
            "count": 1,
            "_links": {"next": None, "previous": None},
        }

        diff = DeepDiff(
            rv.json(),
            expected,
            exclude_regex_paths={r"root\['_embed'\]\['payments'\]\[\d+\]\['id'\]"},
        )
        self.assertEqual(diff, {}, msg=rv.json())

    @freeze_time("2022-06-01")
    def test_get_payment(self):
        payload = {
            "amount": {"currency": "EUR", "value": "100.00"},
            "description": "My first API payment",
            "webhookUrl": "https://webshop.example.org/mollie-webhook/",
            "redirectUrl": "https://webshop.example.org/order/12345/",
        }
        rv = requests.post("http://localhost:3333/v2/payments", json=payload)
        self.assertEqual(rv.status_code, 201, msg=rv.json())

        payment_id = rv.json()["id"]
        rv = requests.get(f"http://localhost:3333/v2/payments/{payment_id}", json=payload)
        self.assertEqual(rv.status_code, 200, msg=rv.json())

        expected = {
            "resource": "payment",
            "amount": {"currency": "EUR", "value": "100.00"},
            "description": "My first API payment",
            "webhookUrl": "https://webshop.example.org/mollie-webhook/",
            "redirectUrl": "https://webshop.example.org/order/12345/",
            "sequenceType": "oneoff",
            "createdAt": "2022-06-01T00:00:00",
            "metadata": None,
            "id": payment_id,
            "status": "open",
        }

        diff = DeepDiff(
            rv.json(),
            expected,
        )
        self.assertEqual(diff, {}, msg=diff)
