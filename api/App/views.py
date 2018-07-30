from flask import Flask, request, jsonify, make_response
from api.models.models import DiaryDatabase
from api.validate import Validate
'''Initialising a flask application'''
app = Flask(__name__)
'''Initialising an empty dictionary'''
import datetime

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

                     
# entries = []
# ''' get all entries'''
# @app.route('/api/v1/entries', methods=['GET'])
# def api_all():
#     return jsonify(entries),200

# ''' get single entry'''
# @app.route('/api/v1/entries/<int:entry_id>', methods=['GET'])
# def get_task(entry_id):

#     data = "INVALID URL, OR RECORD DOESNT EXIST: TRY AGAIN!"
#     response = jsonify({"entries": data})
#     response.status_code = 404
#     for entry in entries:
#         if entry['id'] == entry_id:
#             response = jsonify({"entries": entry})
#             response.status_code = 200
#     return response
    
# '''post an entry'''
# @app.route('/api/v1/entries', methods=['POST'])
# def create_entry():
#     data = request.get_json()
#     valid = Validate(data["name"], data["purpose"])
#     info = valid.validate_entry()
#     entry = {}
#     if info is True:
#         entry = {
#             "id": len(entries) + 1,
#             "name": data["name"],
#             "purpose": data["purpose"],
#             "date_created": now.strftime("%Y-%m-%d"),
#             "type": data["type"],
#             "due_date": data["due_date"],}
#         entries.append(entry)
#         response = jsonify({"message": "Entry saved", "entry": entry})
#         response.status_code = 201
#         return response
#     else:
#         response = jsonify({"message": "INVALID OR MISSING DATA FIELDS, NAME AND PURPOSE SHOULD BE PROVIDED"})
#         response.status_code = 400
#         return response


# '''modify an entry using its id'''
# @app.route('/api/v1/entries/<int:entry_id>', methods=['PUT'])
# def update_entry(entry_id):
#     data = request.get_json()
#     valid = Validate(data["name"],data["purpose"])
#     info = valid.validate_entry()

#     for entry in entries:
#         if info is True and entry['id'] == entry_id:
        
#             entry['name'] = data['name']
#             entry['purpose'] = data['purpose']
#             entry['date_created'] = now.strftime("%Y-%m-%d") 
#             entry['type'] = data['type']
#             entry['due_date'] = data['due_date']

#             response = jsonify({"message": "RECORD UPATED","entry":entry})
#             response.status_code = 200
#             return response
#         else:
#             response = jsonify({"message": "INVALID OR MISSING DATA FIELDS, NAME AND PURPOSE SHOULD BE PROVIDED"})
#             response.status_code = 400
#             return response

    