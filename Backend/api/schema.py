from marshmallow import Schema, fields

class ResourceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    arn = fields.Str(required=False)
    value = fields.Str(allow_none=False)
    resource_type = fields.Str(required=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
