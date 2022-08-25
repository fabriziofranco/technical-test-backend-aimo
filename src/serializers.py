from marshmallow import Schema, fields, ValidationError, validates
from models import User, Note

class UserSerializer(Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates("username")
    def username_validations(self, value):
        if len(value) > 20:
            raise ValidationError("Username must be at most 20 characters")
        
        user = User.select().where(User.username==value)
        if len(user) >0:
            raise ValidationError("Username is already in use")
 

class NoteSerializer(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    creation_date = fields.Date()

    @validates("title")
    def title_validations(self, value):
        if len(value) > 200:
            raise ValidationError("Title must be at most 20 characters")    


class LoginSerializer(Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True)

    @validates("username")
    def username_validations(self, value):       
        user = User.select().where(User.username==value)
        if len(user)==0:
            raise ValidationError("Username is not registered")    


user_schema = UserSerializer()
users_schema = UserSerializer(many=True)
login_schema = LoginSerializer()
note_schema = NoteSerializer()
notes_schema = NoteSerializer(many=True)