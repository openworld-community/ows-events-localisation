from sqlalchemy import text


def search_category(text_to_category, db):
    sql = text(
        f"""
            SELECT category_cache.category_text
            FROM category_cache
            WHERE source_text='{text_to_category}'
            AND category_text IS NOT NULL;
            """
    )
    result = db.session.execute(sql)

    column_names = result.keys()
    data = [dict(zip(column_names, row)) for row in result.fetchall()]
    return data


def last_access_register_category_cache(text_to_category, db):
    sql = text(
        f"""
            UPDATE category_cache
                SET last_access_date=CURRENT_DATE
            WHERE source_text=:text
        """
    )
    db.session.execute(sql, {"text": text_to_category})
    db.session.commit()


def cache_category_text(text_to_category, result, db):
    sql = text(
        f"""
            INSERT INTO category_cache
            (source_text,
            category_text)
            VALUES
            (:text,
            :result);
        """
    )
    db.session.execute(
        sql, {"text": text_to_category, "result": result}
    )
    db.session.commit()
