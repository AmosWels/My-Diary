from flask import  request, jsonify, make_response
'''Initialising a flask application'''
app = Flask(__name__)
'''Initialising an empty dictionary'''
entries = []

@app.route('/GET/entries', methods=['GET'])
def api_all():
    return jsonify(entries),200

@app.route('/GET/entries/<int:entry_id>', methods=['GET'])
def get_task(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        return make_response(jsonify({"result": "No Entry with id"})), 400
    else:
        return jsonify({'entry': entry[0]}),200

@app.route('/POST/entries', methods=['POST'])
def create_entry():
    if not 'name' and 'purpose' and 'id' and 'date_created' and 'type' and 'due_date' in request.json:
        return make_response(jsonify({"result":"Empty Records Detected"})), 400
    else:
        entry = {
            'id': request.json['id'],
            'name': request.json['name'],
            'purpose': request.json.get('purpose', ""),
            'date_created': request.json['date_created'],
            'type': request.json['type'],
            'due_date': request.json['due_date'],
        }
        entries.append(entry)
        return jsonify({'entry': entry}), 201

@app.route('/PUT/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    ent = [entry for entry in entries if (entry['id'] == entry_id)]
    
    if not 'name' in request.json:
        return make_response(jsonify({"result":"Empty Name record update"})), 400
    elif 'name' in request.json : 
        ent[0]['name'] = request.json['name']

    if not 'purpose' in request.json:
        return make_response(jsonify({"result":"Empty purpose record update"})), 400
    elif 'purpose' in request.json : 
        ent[0]['purpose'] = request.json['purpose']  

    if not 'date_created' in request.json:
         return make_response(jsonify({"result":"Empty date_created record update"})), 400   
    elif 'date_created' in request.json : 
        ent[0]['date_created'] = request.json['date_created'] 
    
    if not 'type' in request.json:
         return make_response(jsonify({"result":"Empty type record update"})), 400  
    elif 'type' in request.json : 
        ent[0]['type'] = request.json['type'] 

    if not 'due_date' in request.json:
         return make_response(jsonify({"result":"Empty due_date record update"})), 400
    if 'due_date' in request.json : 
        ent[0]['due_date'] = request.json['due_date'] 

    return jsonify({'entry': ent[0]}),200
