import os

from flask import request, abort

from root.auth import is_authorized

from root.database import db

from flask import Blueprint

from root.db.text.seo_optimisation_controller import seoOptimisationController
from root.translate_query import search_text, last_access_register, cache_text
from mtranslate import translate

text_router = Blueprint("Text", __name__)


@text_router.route("/")
@text_router.route("/translated_text")
def translated_text():
    AUTH = os.getenv("AUTH")
    authorization_header = request.headers.get("Authorization")

    if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
    ):
        abort(403)
    args = request.args

    text_to_translate = args.get("text")
    target_language = args.get("tl")

    if not text_to_translate:
        return "No text"

    if not target_language:
        return "No target language"

    search_result = search_text(
        text_to_translate=text_to_translate,
        table="translation_result",
        language=target_language,
        db=db,
    )

    if search_result:
        result = search_result[0]["translated_text"]
        last_access_register(
            text_to_translate=text_to_translate,
            table="translation_result",
            language=target_language,
            db=db,
        )
    else:
        result = translate(text_to_translate, target_language)
        cache_text(
            text_to_translate=text_to_translate,
            table="translation_result",
            language=target_language,
            result=result,
            db=db,
        )

    return result


@text_router.route("/get_seo_optimised_text", methods=["POST"])
def get_seo_optimised_text():
    AUTH = os.getenv("AUTH")
    authorization_header = request.headers.get("Authorization")

    if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
    ):
        abort(403)

    language = request.form.get("language")
    text = request.form.get("text")

    if not language:
        return "No language"

    if language not in ["en", "ru"]:
        return "Wrong language, only en and ru are supported"

    if not text:
        return "No text"

    return seoOptimisationController.get_text(text, language)