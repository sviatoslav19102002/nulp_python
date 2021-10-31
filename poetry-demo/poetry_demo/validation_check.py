from marshmallow import Schema, fields
from marshmallow.validate import Length, Range


class UserSchema(Schema):
    first_name = fields.String(validate=Length(min=3))
    second_name = fields.String(validate=Length(min=3))
    username = fields.String(validate=Length(min=3))
    password = fields.String(validate=Length(min=6))
    email = fields.Email()


class WalletSchema(Schema):
    name = fields.String(validate=Length(min=3))
    amount = fields.Integer(strict=True)
    owner_id = fields.Integer(strict=True)


class TransferSchema(Schema):
    purpose = fields.String()
    fr0m_id = fields.Integer(strict=True)
    to_id = fields.Integer(rstrict=True)
    amount = fields.Integer(strict=True)