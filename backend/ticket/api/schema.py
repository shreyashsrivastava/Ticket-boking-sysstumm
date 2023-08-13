from marshmallow import Schema, fields, validate

class TicketSchema(Schema):
    id = fields.Int(required=False, dump_only=True)
    user = fields.Int(required=False, dump_only=True)
    date = fields.Date(required=True)
    show = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))