from marshmallow import Schema, fields, validate

class CreateUserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Str(required=True)
    dob = fields.Date(format="%Y-%m-%d", required=True)
    phone = fields.Int(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=5))
    
class LoginUserSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=5))