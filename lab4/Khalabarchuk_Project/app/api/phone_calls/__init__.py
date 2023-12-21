from flask import Blueprint
from flask_restful import Api
from marshmallow import ValidationError

from .resource import CRUDPhoneCallsResource, PhoneCallsResource

api_phone_calls_bp = Blueprint("api_phone_calls", __name__)

api = Api(api_phone_calls_bp, errors=api_phone_calls_bp.app_errorhandler)

api.add_resource(PhoneCallsResource, "/")
api.add_resource(CRUDPhoneCallsResource, "/<int:id>")


@api_phone_calls_bp.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return e.messages, 400
