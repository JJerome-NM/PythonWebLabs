from flask import request
from flask_restful import Resource

from .schemas import UserSchema
from app.authentication.entitys import AuthUser
from ... import db


class ManyUsersResource(Resource):

    def get(self):
        return UserSchema(many=True).dump(AuthUser.query.all())

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return schema.dump(user)


class UserResource(Resource):

    def get(self, id):
        user = AuthUser.query.get(id)

        if not user:
            return {
                "message": "User not found"
            }, 404

        return UserSchema(partial=True).dump(user)

    def put(self, id):
        schema = UserSchema()
        user = AuthUser.query.get(id)

        if not user:
            return {
                "message": "User not found"
            }, 404

        user = schema.load(request.json, instance=user)

        db.session.add(user)
        db.session.commit()

        return schema.dump(user)

    def delete(self, id):
        user = AuthUser.query.get(id)

        if not user:
            return {
                "message": "User not found"
            }, 404

        db.session.delete(user)
        db.session.commit()

        return {"message": f"User {user.username} deleted"}

