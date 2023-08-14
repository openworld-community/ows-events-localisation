from functools import wraps

from flask import request, jsonify
import jwt

from root.config import settings


def token_required(f):

    """Декоратор для проверки аутентифицирован ли пользователь
        Служит для защиты определенных ресурсов

        Можно накинуть на апи этот декоратор и если пользователь незалогиненый
        то выпадет ошибка


        На данный момент не рабочий :)

        """

    @wraps(f)
    def decorator():
        token = request.headers.get('token')
        if not token:
            return jsonify({'message': 'Токен отсутствует'}), 401
        try:
            data = jwt.decode(token, settings.SECRET_KEY, "HS256")
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Токен недействителен'}), 403
        return f(current_user)

    return decorator

