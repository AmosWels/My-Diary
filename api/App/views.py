from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
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
        response = jsonify({"MESSAGE":"CREATED "})
        response.status_code = 201
        return response
    else:
        response = jsonify({"MESSAGE":"USERNAME IS INVALID, OR ALREADY TAKEN UP! KINDLY PROVIDE ANOTHER USERNAME"})
        response.status_code = 400
        return response

@app.route('/api/v1/users/signin', methods=['POST'])
def signin():
    """user login"""
    data = request.get_json()
    Lusername = data["username"]
    Lpassword = data["password"]
    valid = Validate(Lusername, Lpassword)
    check = db_connect.signin(Lusername, Lpassword)
    if valid.validate_entry():
        user = db_connect.signin(Lusername, Lpassword)
        return user
        return make_response(jsonify(response)), 200
    else:
        return jsonify({"MESSAGE":"YOUR CREDENTIALS ARE WRONG! PLEASE CHECK YOUR DATA FIELD."})
    
@app.route('/api/v1/users/create', methods=['POST'])
@jwt_required
def create_user_entry():
    """create user entries """
    entrydata = request.get_json()
    authuser = get_jwt_identity()
    entrydata["user_id"] = authuser["user_id"]
    valid = Validate(entrydata["name"], entrydata["purpose"])
    info = valid.validate_entry()
    if info is True:
        info = db_connect.create_user_entries(entrydata["name"], entrydata["due_date"], entrydata["type"], entrydata["purpose"],entrydata["user_id"])
        return info
    else:
        response = jsonify({"MESSAGE": "SHOULD PROVIDE NAME AND PURPOSE OF ENTRY!"})
        response.status_code = 400
        return response         
@app.route('/api/v1/users/entry/<int:entry_id>', methods=['GET'])
@jwt_required
def get_single_entries(entry_id):
    """get all user entries"""
    authuser = get_jwt_identity()
    entryUSER = authuser["user_id"]
    db_connect.cursor.execute("SELECT * FROM tdiaryentries where user_id = %s and id = %s ", (entryUSER, entry_id))
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    if result > 0:
        entry = db_connect.get_single_user_entry(entryUSER,entry_id)
        return entry
    else:
        response = jsonify({"MESSAGE": "YOUR DONT HAVE A SPECIFIC ENTRY WITH THAT ID!"})
        response.status_code = 400
        return response 

@app.route('/api/v1/users/allentries', methods=['GET'])
@jwt_required
def get_user_entries():
    """get all user entries"""
    authuser = get_jwt_identity()
    entryUSER = authuser["user_id"]
    entries = db_connect.get_all_user_entries(entryUSER)
    return entries

@app.route('/api/v1/users/modify/<int:entry_id>', methods=['PUT'])
@jwt_required
def update_user_entry(entry_id):
    entrydata = request.get_json()
    authuser = get_jwt_identity()
    entryUSER = authuser["user_id"]
    valid = Validate(entrydata["name"], entrydata["purpose"])
    check = valid.validate_entry()
    if check is True:
        db_connect.cursor.execute("SELECT * FROM tdiaryentries where user_id = %s and id = %s ", (entryUSER, entry_id))
        db_connect.conn.commit()
        result = db_connect.cursor.rowcount
        if result > 0:
            entry = db_connect.update_user_entryid(entryUSER, entry_id, entrydata["name"], entrydata["due_date"], entrydata["type"], entrydata["purpose"])
            return entry
        else:
            response = jsonify({"MESSAGE": "YOUR DONT HAVE A SPECIFIC ENTRY WITH THAT ID!"})
            response.status_code = 400
            return response 
    else:
        response = jsonify({"MESSAGE": "SHOULD PROVIDE NAME AND PURPOSE OF ENTRY!"})
        response.status_code = 400
        return response  


