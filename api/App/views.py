from flask import Flask, request, jsonify, make_response
'''Initialising a flask application'''
app = Flask(__name__)
'''Initialising an empty dictionary'''
import datetime

now = datetime.datetime.now()

entries = []
''' get all entries'''
@app.route('/GET/entries', methods=['GET'])
def api_all():
    return jsonify(entries),200

''' get single entry'''
@app.route('/GET/entries/<int:entry_id>', methods=['GET'])
def get_task(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        return make_response(jsonify({"result": "No Entry with that id"})), 400
    return jsonify({'entry': entry[0]}),200
    
'''post an entry'''
@app.route('/POST/entries', methods=['POST'])
def create_entry():
    if 'name' and 'purpose' and 'id' and 'date_created' and 'type' and 'due_date' in request.json:
        entry = {
            'id': len(entries) + 1,
            'name': request.json['name'],
            'purpose': request.json.get('purpose', ""),
            'date_created': now.strftime("%Y-%m-%d"),
            'type': request.json['type'],
            'due_date': request.json['due_date'],
        }
        entries.append(entry)
    else:
        return make_response(jsonify({"result":"Empty Records Detected"})), 400
    return jsonify({'entry': entry}), 201

'''modify an entry using its id'''
@app.route('/PUT/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    ent = [entry for entry in entries if (entry['id'] == entry_id)]
    
    if 'name' and 'purpose' and 'date_created' and 'type'and 'due_date' in request.json:
        
        ent[0]['name'] = request.json['name']
        ent[0]['purpose'] = request.json['purpose']
        ent[0]['date_created'] = now.strftime("%Y-%m-%d") 
        ent[0]['type'] = request.json['type']
        ent[0]['due_date'] = request.json['due_date']
    else:
        return make_response(jsonify({"result":"Empty record update"})), 400

    return jsonify({'entry': ent[0]}),200