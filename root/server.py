from path import Path

from flask import Flask, request, abort
from dotenv import load_dotenv

import os
from os.path import join, dirname

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
    if cursor.rowcount>0:
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
    if token_from_request==token_to_validate:
        return True
    return False


def create_app():
    app = Flask(__name__)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    @app.route("/")
    def hello():

        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWORD")
        HOST = os.getenv("HOST")
        PORT = os.getenv("PORT")
        DB = os.getenv("DB")
        TABLE = os.getenv("TABLE")
        AUTH = os.getenv("AUTH")

        authorization_header = request.headers.get('Authorization')

        if not is_authorized(
                token_to_validate = AUTH,
                token_from_request = authorization_header
            ):
            abort(403)

        args = request.args

        text = args.get('text')
        target_language = args.get('tl')

        try:
            conn = pg.connect(
                host=HOST,
                database=DB,
                port=PORT,
                user=USER,
                password=PASSWORD,
                sslmode='disable',
            )
            conn.autocommit = True
        except:
            return "No database connection"
        
        if not text:
            return "No text"

        if not target_language:
            return "No target language"
        
        cursor = conn.cursor()
        
        search_result = search_text(
            text=text,
            table=TABLE,
            language=target_language,
            cursor=cursor
        )

        if search_result:
            result=search_result
            last_access_register(
                text=text,
                table=TABLE,
                language=target_language,
                cursor=cursor
            )
        else:
            result = translate(text, target_language)
            cache_text(
                text=text,
                table=TABLE,
                language=target_language,
                result=result,
                cursor=cursor
            )

        return result

    return app


if __name__ == "__main__":

    create_app().run(host="0.0.0.0")
