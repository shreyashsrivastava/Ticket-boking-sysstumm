from marshmallow import Schema, fields, validate

class VenueSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    place = fields.Str(required=False, validate=validate.Length(min=1))
    capacity = fields.Int(required=False, validate=validate.Range(min=1))
    screens = fields.Int(required=True, validate=validate.Range(min=1))
    
class SearchSchema(Schema):
    search = fields.Str(required=True, validate=validate.Length(min=3))