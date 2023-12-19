from marshmallow import validate, ValidationError, validates_schema, fields

from ... import mm
from ...authentication.entitys import AuthUser


class UserSchema(mm.SQLAlchemySchema):
    class Meta:
        model = AuthUser
        load_instance = True

    username = fields.String(required=True, validate=[validate.Length(min=4)])
    email = fields.String(required=True, validate=[validate.Email()])
    password = fields.String(required=True, validate=[validate.Length(min=6)])

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get('email')
        if AuthUser.query.filter_by(email=email).first():
            raise ValidationError(f"Email {email} already exists")

    @validates_schema
    def validate_username(self, data, **kwargs):
        username = data.get('username')
        if AuthUser.query.filter_by(username=username).first():
            raise ValidationError(f"Username {username} already exists")
