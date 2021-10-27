from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    first_name = fields.String(required=True, validate=Length(min=3))
    second_name = fields.String(required=True, validate=Length(min=3))
    username = fields.String(required=True, validate=Length(min=3))
    password = fields.String(required=True, validate=Length(min=6))
    email = fields.Email(required=True)


class WalletSchema(Schema):
    name = fields.String(required=True, validate=Length(min=3))
    amount = fields.Integer(strict=True)
    owner_id = fields.Integer(required=True, strict=True)


class TransferSchema(Schema):
    purpose = fields.String()
    fr0m_id = fields.Integer(strict=True)
    to_id = fields.Integer(rstrict=True)
    amount = fields.Integer(strict=True)