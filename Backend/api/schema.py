from marshmallow import Schema, fields

class NamespaceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ResourceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    arn = fields.Str(required=True)
    value = fields.Str()
    resource_type = fields.Str()
    namespace = fields.Str(required=True)
