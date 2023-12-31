from flask import request
from flask_restful import Resource

from app import db
from app.api.auth.JWTUtils import JWTUtils
from app.api.phone_calls.entitys import PhoneCall
from app.api.phone_calls.schema import PhoneCallSchema
from app.authentication.entitys import AuthUser


class PhoneCallsResource(Resource):
    @JWTUtils.verify_token
    def get(self):
        return PhoneCallSchema(many=True).dump(PhoneCall.query.all())

    @JWTUtils.verify_token
    def post(self):
        schema = PhoneCallSchema()
        call = schema.load(request.json)

        db.session.add(call)
        db.session.commit()

        return schema.dump(call)


class CRUDPhoneCallsResource(Resource):

    @JWTUtils.verify_token
    def get(self, id):
        call = PhoneCall.query.get(id)

        if not call:
            return {
                "message": "Phone call not found"
            }, 404

        return PhoneCallSchema().dump(call)

    @JWTUtils.verify_token
    def put(self, id):
        schema = PhoneCallSchema()
        call = AuthUser.query.get(id)

        if not call:
            return {
                "message": "Phone call not found"
            }, 404

        call = schema.load(request.json, instance=call)

        db.session.add(call)
        db.session.commit()

        return schema.dump(call)

    @JWTUtils.verify_token
    def delete(self, id):
        call = PhoneCall.query.get(id)

        if not call:
            return {
                "message": "Phone call not found"
            }, 404

        db.session.delete(call)
        db.session.commit()

        return {"message": f"Phone call {call.id} deleted"}

