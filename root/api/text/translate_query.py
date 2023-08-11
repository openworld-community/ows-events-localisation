from sqlalchemy import text
from root.database import engine
from root.session import session


def search_text(text_to_translate: str, table: str, language: str):
    sql = text(f"""
            SELECT {table}.translated_text
            FROM {table}
            WHERE source_text='{text_to_translate}'
            AND target_language='{language}'
            AND translated_text IS NOT NULL;
            """
            )

    result = engine.execute(sql)
    column_names = result.keys()
    data = [dict(zip(column_names, row)) for row in result.fetchall()]
    return data


def last_access_register(text_to_translate: str, language: str, table: str):
    sql = text(
        f"""
            UPDATE {table}
                SET last_access_date=CURRENT_DATE
            WHERE source_text=:text
            AND target_language=:language;
        """
    )

    # Используем объект Session для выполнения запроса и коммита транзакции
    session.execute(sql, {"text": text_to_translate, "language": language})

    session.commit()  # commit the transaction


def cache_text(text_to_translate: str, table: str, language: str, result: str):
    sql = text(
        f"""
            INSERT INTO {table}
            (source_text,
            target_language,
            translated_text)
            VALUES
            (:text,
            :language,
            :result);
        """
    )

    # Используем объект Session для выполнения запроса и коммита транзакции
    session.execute(
        sql, {"text": text_to_translate, "result": result, "language": language}
    )
    session.commit()  # commit the transaction
