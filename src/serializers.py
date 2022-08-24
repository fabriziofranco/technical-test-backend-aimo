from marshmallow import Schema, fields, validate

class UserSerializer(Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True)

class NoteSerializer(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    creation_date = fields.Date()