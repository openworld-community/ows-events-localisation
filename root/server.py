import os
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS

from sqlalchemy import text
from mtranslate import translate

def search_text(text_to_translate, table, language, db):
    sql = text(f"""
            SELECT {table}.translated_text
            FROM {table}
            WHERE source_text='{text}'
            AND target_language='{language}'
            AND translated_text IS NOT NULL;
            """)
    result = db.session.execute(sql, {
        'text': text_to_translate,
        'language': language
        })
    column_names = result.keys()
    data = [dict(zip(column_names, row)) for row in result]
    return data
    
def last_access_register(text_to_translate, language, table, db):
    sql = text(f"""
            UPDATE {table}
                SET last_access_date=CURRENT_DATE
            WHERE source_text=:text
            AND target_language=:language;
        """)
    db.session.execute(sql, {
        'text': text_to_translate,
        'language': language
    })
    db.session.commit()

def cache_text(text_to_translate, table, language, result, db):
    sql = text(f"""
            INSERT INTO {table}
            (source_text,
            target_language,
            translated_text)
            VALUES
            (:text,
            :language,
            :result);
        """)
    db.session.execute(sql, {
        'text': text_to_translate,
        'result': result,
        'language': language
    })
    db.session.commit()

def is_authorized(token_from_request, token_to_validate):
    # two validations in case both tokens are None for some reason
    return token_from_request and token_from_request==token_to_validate

def create_app():
    app = Flask(__name__)
    CORS(app)

    load_dotenv('.env')

    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")
    DB = os.getenv("DB")

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?sslmode=disable'
    db = SQLAlchemy(app)
    
    @app.route("/")
    def hello():
        TABLE = os.getenv("TABLE")
        AUTH = os.getenv("AUTH")
        authorization_header = request.headers.get('Authorization')
        
        if not is_authorized(
                token_to_validate = AUTH,
                token_from_request = authorization_header
            ):
            abort(403)
        args = request.args

        text_to_translate = args.get('text')
        target_language = args.get('tl')
        
        if not text_to_translate:
            return "No text"

        if not target_language:
            return "No target language"
        
        search_result = search_text(
            text_to_translate=text_to_translate,
            table=TABLE,
            language=target_language,
            db=db
        )

        if search_result:
            result=search_result[0]['translated_text']
            last_access_register(
                text_to_translate=text_to_translate,
                table=TABLE,
                language=target_language,
                db=db
            )
        else:
            result = translate(text_to_translate, target_language)
            cache_text(
                text_to_translate=text_to_translate,
                table=TABLE,
                language=target_language,
                result=result,
                db=db
            )

        return result

    return app


if __name__ == "__main__":

    create_app().run(host="0.0.0.0")
