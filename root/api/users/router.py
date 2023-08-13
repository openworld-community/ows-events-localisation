import os
import sys

from flask import abort, jsonify, request
from sqlalchemy.exc import IntegrityError
from root.api.users.auth import get_password_hash
from root.api.users.user_model import User
from root.auth import is_authorized
from flask import Blueprint
from root.session import session

users_router = Blueprint("Users", __name__)


@users_router.route('/create_user', methods=['POST'])
def create_user():

    """ Апи по созданию пользователя, передавать в Postman нужно username и password_hash
        password_hash - это обычный пароль, а хешируется он в hashed_password """

    AUTH = os.getenv("AUTH")
    authorization_header = request.headers.get("Authorization")
    if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
    ):
        abort(403)

    username = request.form.get("username")
    password_hash = request.form.get("password_hash")

    if not username:
        return "No username"
    if not password_hash:
        return "No password_hash"

    hashed_password = get_password_hash(password_hash)
    new_user = User(username=username, password_hash=hashed_password)

    try:
        session.add(new_user)
        session.commit()
        return jsonify({"message": "User created successfully"})
    except IntegrityError:
        session.rollback()
        return jsonify({"message": "Username already exists"}), 400


@users_router.route('/users', methods=['GET'])
def get_all_users():

    """ Апи по получению всех существующих пользователей """

    AUTH = os.getenv("AUTH")
    authorization_header = request.headers.get("Authorization")
    if not is_authorized(
            token_to_validate=AUTH, token_from_request=authorization_header
    ):
        abort(403)

    users = session.query(User).all()

    # Преобразование пользователей в список словарей
    users_list = [
        {"id": user.user_id, "username": user.username}
        for user in users
    ]

    session.close()

    return users_list


@users_router.route('/delete_user/<int:user_id>', methods=["DELETE"])
def delete_user(user_id: int):

    """ Апи по удалению пользователя, нужно заметить что используется метод DELETE
        Для корректной работы нужно передать id пользователя в адрес запроса """

    deleted_user = session.query(User).filter_by(user_id=user_id).first()
    if deleted_user:
        deleted_user_data = {
            "user_id": deleted_user.user_id,
            "username": deleted_user.username,
            "create_date": deleted_user.create_date,
            "last_access_date": deleted_user.last_access_date
        }
        session.delete(deleted_user)
        session.commit()
        return jsonify({"deleted_user": deleted_user_data})
    else:
        return jsonify({"message": "User not found."}), 404
