import os
from functools import wraps

from dotenv import load_dotenv
from flask import abort, request

load_dotenv()


def check_authorization(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        token_to_validate = os.getenv("AUTH")
        token_from_request = request.headers.get("Authorization")

        if not token_from_request or token_from_request != token_to_validate:
            return abort(403)
        return route(*args, **kwargs)

    return wrapper
