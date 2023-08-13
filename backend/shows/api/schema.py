from marshmallow import Schema, fields, validate

class ShowSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    rating = fields.Int(required=False, validate=validate.Range(min=1, max=5))
    tag = fields.Str(required=False, validate=validate.Length(min=1))
    updated_price = fields.Int(required=True, validate=validate.Range(min=1))
    venue_id = fields.Int(required=True)
    date = fields.Date(required=True)
    tickets_available = fields.Int(required=False, dump_only=True)