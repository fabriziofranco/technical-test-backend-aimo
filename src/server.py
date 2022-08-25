from truckpad.bottle.cors import enable_cors
from peewee import DoesNotExist
from serializers import users_schema, user_schema, note_schema, notes_schema, login_schema
from bottle import run, Bottle, response, request
from models import User, Note
import jwt

app = Bottle()

##############################################
#                                            #
#               Aux functions                #
#                                            #
##############################################

def token_auth(auth_token):
    try:
        decoded = jwt.decode(auth_token, "TOY_SECRET_KEY")['id']
        return User.get(User.id==decoded)
    except (jwt.DecodeError, DoesNotExist):
        return None


##############################################
#                                            #
#                   Users                    #
#                                            #
##############################################


@enable_cors
@app.route('/signup', method=['POST'])
def signup():
    data = user_schema.load(request.json)
    if data.errors:
        response.status= 405
        return {"result": data.errors, "status": response.status_code}
    else:
        username = data.data['username']
        password = data.data['password']
        User.create(username = username, password = password)
        return {"result": "success", "status": response.status_code}

@enable_cors
@app.route('/login', method=['POST'])
def login():
    data = login_schema.load(request.json)
    if data.errors:
        response.status= 405
        return {"result": data.errors, "status": response.status_code}
    else:
        user = User.get(User.username == data.data['username'])
        real_password = user.password    
        user_id = user.id
        if data.data['password'] != real_password:
            response.status= 401
            return {"result": {"password": ["Wrong password"]}, "status": response.status_code}    
        else:
            token = jwt.encode({"username": data.data['username'], "id": user_id},"TOY_SECRET_KEY", algorithm="HS256")
            return {"result": {"token":token}, "status": response.status_code}    
        
        
@enable_cors
@app.route('/users', method=['GET'])
def all_users():
    users = [user['username'] for user in User.select().dicts()]
    return {"result": "success", "status": response.status_code, "users": users}

##############################################
#                                            #
#                  Notes                     #
#                                            #
##############################################

@enable_cors
@app.route('/notes', method=['POST'])
def add_note():
    auth_user = token_auth(request.headers.get('Authorization'))
    if auth_user is None:
        response.status= 401
        return {"result": {"token": ["Wrong token"]}, "status": response.status_code}        
    else:
        data = note_schema.load(request.json)
        if data.errors:
            response.status= 405
            return {"result": data.errors, "status": response.status_code}
        else:
            title = data.data['title']
            Note.create(title = title, user = auth_user)
            return {"result": "success", "status": response.status_code}        


@enable_cors
@app.route('/notes', method=['GET'])
def add_note():
    auth_user = token_auth(request.headers.get('Authorization'))
    if auth_user is None:
        response.status= 401
        return {"result": {"token": ["Wrong token"]}, "status": response.status_code}        
    else:
        selected_notes = Note.select().where(Note.user==auth_user).dicts()
        notes = [{"title": note['title'], "creation_date": str(note['creation_date'])} for note in selected_notes]
        return {"result": "success", "status": response.status_code, "notes": notes}  



run(app, host='localhost', port=8000)