from datetime import datetime, timedelta
import datetime as dt
from functools import wraps

import jwt

from flask import current_app as app, request


class JWTUtils:
    __SECRET_KEY = app.config.get("SECRET_KEY")
    __Algorithm = "HS256"

    @staticmethod
    def generate_token(username: str):
        payload = {
            'exp': datetime.now(dt.UTC) + timedelta(hours=2),
            'iat': datetime.now(dt.UTC),
            'sun': username
        }
        return jwt.encode(payload=payload, key=JWTUtils.__SECRET_KEY, algorithm=JWTUtils.__Algorithm)

    @staticmethod
    def verify_token(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return {'error': 'Token is missing'}, 401

            token = token.split(" ")[1]

            try:
                jwt.decode(token, JWTUtils.__SECRET_KEY, algorithms=[JWTUtils.__Algorithm])
            except jwt.ExpiredSignatureError:
                return {'error': 'Token has expired'}, 401
            except jwt.InvalidTokenError:
                return {'error': 'Invalid token'}, 401

            return func(*args, **kwargs)

        return wrapper
