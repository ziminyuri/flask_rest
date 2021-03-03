from marshmallow import Schema, validate, fields


class UserSchema(Schema):
    email = fields.String(required=True, validate=[validate.Length(max=50)])
    username = fields.String(required=True, validate=[validate.Length(max=50)])
    password = fields.String(required=True)