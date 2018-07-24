from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Create some test data for our catalog in the form of a list of dictionaries.
entries = []

# A route to fetch all entries.
@app.route('/api/v1/resources/entries/all', methods=['GET'])
def api_all():
    return jsonify(entries),200
# A route to fetch a single entry.
@app.route('/api/v1/resources/entries/<int:entry_id>', methods=['GET'])
def get_task(entry_id):
    entry = [entry for entry in entries if entry['id'] == entry_id]
    if len(entry) == 0:
        return make_response(jsonify({"result": "No Entry with id"})), 400
    else:
        return jsonify({'entry': entry[0]}),200
# Post a new entry
@app.route('/api/v1/resources/entries/create', methods=['POST'])
def create_entry():
    if not request.json or not 'name' in request.json:
        return make_response(jsonify({"result":"Bad aRequest"})), 400
    else:
        entry = {
            # 'id': entries[0]['id'] + 1,
            # 'id': entries[-1]['id'] + 1,
            'id': request.json['id'],
            'name': request.json['name'],
            'purpose': request.json.get('purpose', ""),
            'date_created': request.json['date_created'],
            'type': request.json['type'],
            'due_date': request.json['due_date'],
        }
        entries.append(entry)
        return jsonify({'entry': entry}), 201
# update an entry 
@app.route('/api/v1/resources/entries/update/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    ent = [entry for entry in entries if (entry['id'] == entry_id)]
    if 'name' in request.json : 
        ent[0]['name'] = request.json['name']
    if 'purpose' in request.json : 
        ent[0]['purpose'] = request.json['purpose']  
    if 'date_created' in request.json : 
        ent[0]['date_created'] = request.json['date_created'] 
    if 'type' in request.json : 
        ent[0]['type'] = request.json['type'] 
    if 'due_date' in request.json : 
        ent[0]['due_date'] = request.json['due_date'] 
    return jsonify({'entry': ent[0]}),200
