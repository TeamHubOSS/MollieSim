import re
from http import HTTPStatus


class Router:
    registry = set()

    @staticmethod
    def route(method, re_path):
        def decorator(func):
            Router.registry.add((method, re_path, func))
            return func

        return decorator

    @staticmethod
    def handle_route(req_method, req_path, header, body):
        for method, re_path, func in Router.registry:
            if req_method == method and re.match(re_path, req_path):
                return func(req_path, header, body)
        return {}, HTTPStatus.NOT_FOUND
