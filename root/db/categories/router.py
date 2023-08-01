import os

from flask import request, abort

from root.auth import is_authorized
from root.db.categories.category_controller import categories, categoryController


from root.db.categories.category_query import search_category, cache_category_text, last_access_register_category_cache
from root.database import db

from flask import Blueprint


category_router = Blueprint("Category", __name__)


@category_router.route("/get_category", methods=["POST"])
def get_category():
    AUTH = os.getenv("AUTH")
    authorization_header = request.headers.get("Authorization")

    if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
    ):
        abort(403)

    text = request.form.get("text")
    if not text:
        return "No text"

    search_result = search_category(
        text_to_category=text,
        db=db,
    )
    first_item = search_result[0] if len(search_result) else None

    if first_item:
        result = first_item
        last_access_register_category_cache(
            text_to_category=text,
            db=db,
        )
    else:
        result = categoryController.get_category(text)
        cache_category_text(
            text_to_category=text,
            result=result,
            db=db,
        )

    return result


@category_router.route("/get_all_categories", methods=["GET"])
def get_all_categories():
    AUTH = os.getenv("AUTH")
    authorization_header = request.headers.get("Authorization")

    if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
    ):
        abort(403)

    return categories
