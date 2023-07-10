from flask import Flask, request, abort
from dotenv import load_dotenv
from flask_cors import CORS
import os
from os.path import join, dirname
from root.location_description_controller import locationDescriptionController
from root.category_controller import categoryController
from root.seo_optimisation_controller import seoOptimisationController

from mtranslate import translate
import psycopg2 as pg


def search_text(text, table, language, cursor):
    sql = f"""
            SELECT {table}.translated_text
            FROM {table}
            WHERE source_text='{text}'
            AND target_language='{language}'
            AND translated_text IS NOT NULL;
            """
    cursor.execute(sql)
    if cursor.rowcount > 0:
        return cursor.fetchone()[0]
    return None


def last_access_register(text, table, language, cursor):
    sql = f"""
            UPDATE {table}
                SET last_access_date=CURRENT_DATE
            WHERE source_text='{text}'
            AND target_language='{language}';
        """
    cursor.execute(sql)


def cache_text(text, table, language, result, cursor):
    sql = f"""
            INSERT INTO {table}
            (source_text,
            target_language,
            translated_text)
            VALUES
            ('{text}',
            '{language}',
            '{result}');
        """
    cursor.execute(sql)


def is_authorized(token_from_request, token_to_validate):
    if token_from_request == token_to_validate:
        return True
    return False


def create_app():
    app = Flask(__name__)
    CORS(app)

    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

    @app.route("/")
    def hello():
        # TODO: Move creation of connection to a separate function and call it not in every request
        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWORD")
        HOST = os.getenv("HOST")
        PORT = os.getenv("PORT")
        DB = os.getenv("DB")
        TABLE = os.getenv("TABLE")
        AUTH = os.getenv("AUTH")

        authorization_header = request.headers.get("Authorization")

        if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
        ):
            abort(403)

        args = request.args

        text = args.get("text")
        target_language = args.get("tl")

        try:
            conn = pg.connect(
                host=HOST,
                database=DB,
                port=PORT,
                user=USER,
                password=PASSWORD,
                sslmode="disable",
            )
            conn.autocommit = True
        except Exception as e:
            print(e)
            return "No database connection"

        if not text:
            return "No text"

        if not target_language:
            return "No target language"

        text = text.replace("'", "--quote--")

        cursor = conn.cursor()

        search_result = search_text(
            text=text, table=TABLE, language=target_language, cursor=cursor
        )

        if search_result:
            result = search_result
            last_access_register(
                text=text, table=TABLE, language=target_language, cursor=cursor
            )
        else:
            result = translate(text, target_language)
            cache_text(
                text=text,
                table=TABLE,
                language=target_language,
                result=result,
                cursor=cursor,
            )

        return result

    @app.route("/get_category", methods=["POST"])
    def get_category():
        text = request.form.get("text")
        if not text:
            return "No text"

        return categoryController.get_category(text)

    @app.route("/get_description_for_location", methods=["POST"])
    def get_description_for_location():
        language = request.form.get("language")
        location = request.form.get("location")

        if not language:
            return "No language"

        if language not in ["en", "ru"]:
            return "Wrong language, only en and ru are supported"

        if not location:
            return "No location"

        return locationDescriptionController.get_description(location, language)

    @app.route("/get_seo_optimised_text", methods=["POST"])
    def get_seo_optimised_text():
        language = request.form.get("language")
        text = request.form.get("text")

        if not language:
            return "No language"

        if language not in ["en", "ru"]:
            return "Wrong language, only en and ru are supported"

        if not text:
            return "No text"

        return seoOptimisationController.get_text(text, language)

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0")
