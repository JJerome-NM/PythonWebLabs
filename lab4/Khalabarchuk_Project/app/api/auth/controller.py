from flask import request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

from . import api_auth_bp
from .JWTUtils import JWTUtils
from ...authentication.entitys import AuthUser

auth = HTTPBasicAuth(scheme='Bearer')

users = {
    "test": {
        "password": generate_password_hash("test")
    }
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@api_auth_bp.route('/')
@JWTUtils.verify_token
def index():
    return f"Hello username!"


@api_auth_bp.post('/login')
def login():
    user_json = request.json
    user: AuthUser = AuthUser.query.filter_by(username=user_json["username"]).first()

    if user is None:
        return {
            "message": "Username or password is not valid"
        }, 401

    if user.verify_password(user_json["password"]):
        token = JWTUtils.generate_token(username=user_json["username"])
        return {
            "token": token
        }

    return {
        "message": "Invalid username ot password"
    }, 401

