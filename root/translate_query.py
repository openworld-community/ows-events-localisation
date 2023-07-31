from sqlalchemy import text


def search_text(text_to_translate, table, language, db):
    sql = text(
        f"""
            SELECT {table}.translated_text
            FROM {table}
            WHERE source_text='{text_to_translate}'
            AND target_language='{language}'
            AND translated_text IS NOT NULL;
            """
    )
    result = db.session.execute(sql)

    column_names = result.keys()
    data = [dict(zip(column_names, row)) for row in result.fetchall()]
    return data


def last_access_register(text_to_translate, language, table, db):
    sql = text(
        f"""
            UPDATE {table}
                SET last_access_date=CURRENT_DATE
            WHERE source_text=:text
            AND target_language=:language;
        """
    )
    db.session.execute(sql, {"text": text_to_translate, "language": language})
    db.session.commit()


def cache_text(text_to_translate, table, language, result, db):
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
    db.session.execute(
        sql, {"text": text_to_translate, "result": result, "language": language}
    )
    db.session.commit()