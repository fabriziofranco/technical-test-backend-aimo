from serializers import user_schema, user_schema, note_schema, notes_schema
from bottle import run, Bottle, response, request
from models import User, Note
from truckpad.bottle.cors import enable_cors
import jwt


app = Bottle()

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
    
run(app, host='localhost', port=8000)
