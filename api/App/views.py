from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pyisemail import is_email
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from api.models.models import DiaryDatabase
from api.validate import Validate
import jwt
import datetime

'''Initialising a flask application'''
app = Flask(__name__)
'''Initialising cors in flask app'''

CORS(app, resources=r'/api/*')

jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
now = datetime.datetime.now()
db_connect = DiaryDatabase()

@app.route('/api/v1/auth/signup', methods=['POST'])
def register():
    """ registering user """
    data = getjsondata()
    required_fields = {"username", "password"}
    checkfield = Validate.validate_field(data, required_fields)
    if not checkfield:
        username = data["username"]
        password = data["password"]
        valid = Validate(username, password)
        if username.strip() and password.strip() != '' and len(username) >= 5 and len(password) >= 5 and valid.validate_entry():
            db_connect.cursor.execute(
                "SELECT username FROM tusers where username =%s ", (username,))
            db_connect.conn.commit()
            result = db_connect.cursor.rowcount
            if result == 0:
                db_connect.signup(username, password)
                response = jsonify({"Message": "Created Succesfully"})
                response.status_code = 201
                return response
            else:
                response = jsonify(
                    {"Message": "username is invalid, or already taken up! Kindly provide another username"})
                response.status_code = 400
                return response
        else:
            response = jsonify(
                {"Message": "username and password should be provided and *WITH NOT* less than 5 values *EACH*!. Please Avoid such ^{\\s|\\S}*{\\S}+{\\s|\\S}*$ in your username"})
            response.status_code = 400
            return response
    else:
        return jsonify(checkfield), 400

@app.route('/api/v1/auth/login', methods=['POST'])
def signin():
    """user login"""
    data = getjsondata()
    required_fields = {"username", "password"}
    checkfield = Validate.validate_field(data, required_fields)
    if not checkfield:
        username = data["username"]
        password = data["password"]
        valid = Validate(username, password)
        check = db_connect.signin(username, password)
        if valid.validate_entry():
            user = db_connect.signin(username, password)
            return user
    else:
        return jsonify(checkfield), 400

@app.route('/api/v1/entries', methods=['POST'])
@jwt_required
def create_user_entry():
    """create user entries """
    entrydata = getjsondata()
    required_fields = {"due_date", "name", "purpose", "type"}
    checkfield = Validate.validate_field(entrydata, required_fields)
    if not checkfield:
        entrydata["user_id"] = extractuser()
        valid = Validate(entrydata["name"], entrydata["purpose"])
        try:
            date_format = "%Y-%m-%d"
            date_obj = datetime.datetime.strptime(
                entrydata["due_date"], date_format)
            info = valid.validate_entry()
            if info is True and entrydata["name"].isalpha() and entrydata["type"].isalpha():
                info = db_connect.create_user_entries(
                    entrydata["name"], entrydata["due_date"], entrydata["type"], entrydata["purpose"], entrydata["user_id"])
                return info
            else:
                return wrongname_purpose()
        except ValueError:
            return wrongdate_format()
    else:
        return jsonify(checkfield), 400

@app.route('/api/v1/entries/<entry_id>', methods=['GET'])
@jwt_required
def get_single_entries(entry_id):
    """get all user entries"""
    entryUSER = extractuser()
    db_connect.cursor.execute(
        "SELECT * FROM tdiaryentries where user_id = %s and id = %s ", (entryUSER, entry_id))
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    if result > 0:
        entry = db_connect.get_single_user_entry(entryUSER, entry_id)
        return entry
    else:
        response = jsonify(
            {"Message": "You dont have a specific entry with that *id*!"})
        response.status_code = 400
        return response

def extractuser():
    authuser = get_jwt_identity()
    entryUSER = authuser["user_id"]
    return entryUSER

@app.route('/api/v1/entries', methods=['GET'])
@jwt_required
def get_user_entries():
    """get all user entries"""
    entryUSER = extractuser()
    db_connect.cursor.execute(
        "SELECT * FROM tdiaryentries where user_id = %s", [entryUSER])
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    if result > 0:
        entries = db_connect.get_all_user_entries(entryUSER)
        return entries
    else:
        response = jsonify(
            {"Message": "You haven't created any entries yet. Please create first."})
        response.status_code = 200
        return response


@app.route('/api/v1/entries/<entry_id>', methods=['PUT'])
@jwt_required
def update_user_entry(entry_id):
    entrydata = getjsondata()
    required_fields = {"due_date", "name", "purpose", "type"}
    checkfield = Validate.validate_field(entrydata, required_fields)
    if not checkfield:
        entryUSER = extractuser()
        valid = Validate(entrydata["name"], entrydata["purpose"])
        check = valid.validate_entry()
        today_date = now.strftime("%Y-%m-%d")
        try:
            date_format = "%Y-%m-%d"
            date_obj = datetime.datetime.strptime(entrydata["due_date"], date_format)
            db_connect.cursor.execute(
                "SELECT * FROM tdiaryentries where user_id = %s and id = %s ", (entryUSER, entry_id))
            db_connect.conn.commit()
            result = db_connect.cursor.rowcount
            resultdata = db_connect.cursor.fetchone()
            if check is True and entrydata["name"].isalpha() and entrydata["type"].isalpha() and result > 0 and resultdata[5] == today_date:
                entry = db_connect.update_user_entryid(
                    entryUSER, entry_id, entrydata["name"], entrydata["due_date"], entrydata["type"], entrydata["purpose"])
                return entry
            else:
                return wrongname_purpose()
        except ValueError:
            return wrongdate_format()
    else:
        return jsonify(checkfield), 400

def wrongdate_format():
    response = jsonify(
        {"Message": "Please Check that your date format suits this format (YYYY-MM-DD)"})
    response.status_code = 400
    return response

def wrongname_purpose():
    response = jsonify(
        {"Message": "Please provide a *name* and *purpose* of entry. Note You can only modify Today's entries!!"})
    response.status_code = 400
    return response

@app.route('/api/v1/entries/<entry_id>', methods=['DELETE'])
@jwt_required
def delete_user_entry(entry_id):
    entryUSER = extractuser()
    db_connect.cursor.execute("SELECT * FROM tdiaryentries where user_id = %s and id = %s ", (entryUSER, entry_id))
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    if result > 0:
        result = db_connect.delete_user_entryid(entryUSER, entry_id)
        return result
    else:
        response = jsonify(
            {"Message": "You dont have a specific entry with that id to be **Deleted**!"})
        response.status_code = 400
        return response

@app.route('/api/v1/authuser', methods=['GET'])
@jwt_required
def get_user():
    result, user = getuser_count()
    if result > 0:
        userresult = db_connect.get_user(user)
        return userresult
    else:
        return userprofileerror()

def getuser_count():
    user = extractuser()
    db_connect.cursor.execute("SELECT * FROM tusers where id = %s ", (user,))
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    return result, user

@app.route('/api/v1/authuser/profile', methods=['GET'])
@jwt_required
def get_user_profile():
    user = extractuser()
    db_connect.cursor.execute("SELECT * FROM tuserprofile where user_id = %s ", (user,))
    db_connect.conn.commit()
    result = db_connect.cursor.rowcount
    if result > 0:
        userinfo = db_connect.get_user_profile(user)
        return userinfo
    else:
        return userprofileerror()

def userprofileerror():
    response = jsonify(
        {"Message": "No user found"})
    response.status_code = 400
    return response

@app.route('/api/v1/authuser/countentry', methods=['GET'])
@jwt_required
def get_user_count():
    result, user = getuser_count()
    if result > 0:
        result = db_connect.get_entry_count(user)
        return result
    else:
        return userprofileerror()

@app.route('/api/v1/authuser/profile', methods=['POST'])
@jwt_required
def create_user_profile():
    """create user profile """
    checkfield, entrydata = getuserprofile()
    if not checkfield:
        info = getuservalidateentry(entrydata)
        if info is True and entrydata["surname"].isalpha() and entrydata["givenname"].isalpha() and is_email(entrydata["email"]):
            info = db_connect.create_user_prof(
                entrydata["surname"],entrydata["givenname"], entrydata["email"], entrydata["phonenumber"], entrydata["user_id"])
            return info
        else:
            return usererrorinput()
    else:
        return jsonify(checkfield), 400

def getuserprofile():
    entrydata = getjsondata()
    required_fields = {"surname", "givenname", "email", "phonenumber"}
    checkfield = Validate.validate_field(entrydata, required_fields)
    return checkfield, entrydata

def getuservalidateentry(entrydata):
    entrydata["user_id"] = extractuser()
    valid = Validate(entrydata["surname"], entrydata["givenname"])
    info = valid.validate_entry()
    return info

def usererrorinput():
    response = jsonify(
        {"Message": "Please provide a valid *names* and *email* of profile!"})
    response.status_code = 400
    return response

def getjsondata():
    entrydata = request.get_json()
    return entrydata
    
@app.route('/api/v1/authuser/profile', methods=['PUT'])
@jwt_required
def update_user_profile():
    checkfield, entrydata = getuserprofile()
    if not checkfield:
        info = getuservalidateentry(entrydata)
        if info is True and entrydata["surname"].isalpha() and entrydata["givenname"].isalpha() and is_email(entrydata["email"]):
            info = db_connect.update_user_prof(
                entrydata["surname"],entrydata["givenname"], entrydata["email"], entrydata["phonenumber"], entrydata["user_id"])
            return info
        else:
            return usererrorinput()
    else:
        return jsonify(checkfield), 400