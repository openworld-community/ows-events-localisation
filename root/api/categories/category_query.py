from sqlalchemy import text

from root.database import engine
from root.session import session


def search_category(text_to_category: str):
    checked_text = text_to_category.replace("'", "''")
    sql = text(
        f"""
                SELECT category_cache.category_text
                FROM category_cache
                WHERE source_text='{checked_text}'
                AND category_text IS NOT NULL;
               """
    )
    result = engine.execute(sql)
    column_names = result.keys()
    data = [
        dict(zip(column_names, row)) for row in result.fetchall()
    ]  # вернуть первую категорию
    return data


def last_access_register_category_cache(text_to_category: str):
    sql = text(
        f"""
            UPDATE category_cache
                SET last_access_date=CURRENT_DATE
            WHERE source_text='{text_to_category}'
        """
    )
    # Используем объект Session для выполнения запроса и коммита транзакции
    session.execute(sql)

    session.commit()  # commit the transaction


def cache_category_text(text_to_category: str, result: str):
    sql = text(
        f"""
            INSERT INTO category_cache
            (source_text,
            category_text)
            VALUES
            (
            '{text_to_category}',
            '{result}',
            );
        """
    )
    # Используем объект Session для выполнения запроса и коммита транзакции
    session.execute(sql)
    session.commit()  # commit the transaction
