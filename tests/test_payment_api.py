import time
import requests

from deepdiff import DeepDiff
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
                        "amount": {"currency": "EUR", "value": "100.00"},
                        "description": "My first API payment",
                        "webhookUrl": "https://webshop.example.org/mollie-webhook/",
                        "redirectUrl": "https://webshop.example.org/order/12345/",
                        "sequenceType": "oneoff",
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
