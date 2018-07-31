from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
# from flask_jwt_extended import JWTManager
from api.models.models import DiaryDatabase
from api.validate import Validate
import jwt
from functools import wraps
# from App import app

import datetime
# app.config['SECRET_KEY']='thisisasecretkey'
'''Initialising a flask application'''
app = Flask(__name__)
'''Initialising an empty dictionary'''
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
now = datetime.datetime.now()
db_connect = DiaryDatabase()

def __init__(self):
        DiaryDatabase.__init__(self)
        
@app.route('/api/v1/users/signup', methods=['POST'])
def register():
    """ registering user """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    db_connect.cursor.execute("SELECT username FROM tusers where username =%s ", (username, ))
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    if result == 0:
        db_connect.signup(username,password)
        response = jsonify({"message":"Created "})
        response.status_code = 201
        return response
    else:
        response = jsonify({"message":"username is Invalid, or already taken up! Kindly Provide another username"})
        response.status_code = 400
        return response

@app.route('/api/v1/users/signin', methods=['POST'])
def signin():
    """user login"""
    # data = request.get_json()
    # Lpassword = data["password"]
    # auth = request.authorization

    # if  auth and auth.password == 'password':
    #     token = jwt.encode({'user':auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    #     return jsonify({'token':token.decode('UTF-8')})
    # else:
    #     # response = ({"message":"Check data Fields"})
    #     # response.status_code = 404
    #     return make_response('couldnot verify',401,{'www-Authenticate':'Basic realm= "Login required"'})

    data = request.get_json()
    Lusername = data["username"]
    Lpassword = data["password"]
    valid = Validate(Lusername, Lpassword)
    check = db_connect.signin(Lusername, Lpassword)
    # user = db_connect.query.filter_by(username=Lusername).first()
    print (check)
    print (Lusername)
    print(db_connect.signin(Lusername, Lpassword))
    # print (db_connect.generate_token(Lusername))
    if valid.validate_entry():
        info = db_connect.signin(Lusername, Lpassword)
        return info
        # access_token = db_connect.generate_token(Lusername)
        # response = {'message': 'You logged in successfully.','access_token': db_connect.decode_token(access_token)}
        return make_response(jsonify(response)), 200

    else:
        return jsonify({"message":"Check data Fields, Wrong Credentials"})
                    