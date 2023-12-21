from marshmallow import fields, validate
from app import mm
from .entitys import PhoneCall


class PhoneCallSchema(mm.SQLAlchemySchema):
    class Meta:
        model = PhoneCall
        load_instance = True

    first_caller = fields.String(required=True, validate=[validate.Length(min=8)])
    second_caller = fields.String(required=True, validate=[validate.Length(min=8)])
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
