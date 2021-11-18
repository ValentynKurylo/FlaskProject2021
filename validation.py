from marshmallow import Schema, fields
from marshmallow.validate import Length

class WorkerSchema(Schema):
    name = fields.String(validate=Length(min=4))
    login = fields.Email()
    password = fields.String(validate=Length(min=8))
    role = fields.String()


class UserSchema(Schema):
    name = fields.String(validate=Length(min=4))
    login = fields.Email()
    password = fields.String(validate=Length(min=8))
    role = fields.String()


class ProductSchema(Schema):
    name = fields.String()
    price = fields.Float()
    number = fields.Integer()


class OrderSchema(Schema):
    user_id = fields.Integer()
    product_id = fields.Integer()
    number = fields.Integer()


class ProductDemandSchema(Schema):
    user_id = fields.Integer()
    product_id = fields.Integer()
    nameProduct = fields.String()