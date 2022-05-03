import re
from http import HTTPStatus


from molliesim.api import parse_body
from molliesim.api.utils import paginate
from molliesim.router import Router
from molliesim.storage import PaymentStorage

from .models import Payment, PaymentCreate


class PaymentEndpoints:
    LIST = "/v2/payments/?$"
    CREATE = "/v2/payments/?$"
    READ = "/v2/payments/([^/]+)/?$"
    # UPDATE = "/v2/payments/([^/]+)/?$"
    # DELETE = "/v2/payments/([^/]+)/?$"

    @Router.route("POST", CREATE)
    def create(path, headers, body):
        p = Payment(**parse_body(PaymentCreate, body).dict())
        PaymentStorage().set(p)
        return p.dict(), HTTPStatus.CREATED

    @Router.route("GET", LIST)
    def list(path, headers, body):
        payments = PaymentStorage().list()
        return paginate("payments", [p.dict() for p in payments]), HTTPStatus.OK

    @Router.route("GET", READ)
    def read(path, headers, body, payment_id):
        payment = PaymentStorage().get(payment_id)
        if payment:
            return payment.dict(), HTTPStatus.OK
        return {}, HTTPStatus.NOT_FOUND

    # @Router.route("PUT", UPDATE)
    # def update(path, headers, body):
    #     return {"func": "update", "path": path}, HTTPStatus.OK

    # @Router.route("DELETE", DELETE)
    # def delete(path, headers, body):
    #     return {"func": "delete", "path": path}, HTTPStatus.OK
