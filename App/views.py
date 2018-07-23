from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Create some test data for our catalog in the form of a list of dictionaries.
entries = [
    {'id': 0,
     'name': 'Meet Susan',
     'date_created': '24/Aug/2016',
     'type': 'Office',
     'purpose': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been th',
     'due_date': '02/september/2018'},
    {'id': 1,
     'name': 'Meet John',
     'date_created': '24/Aug/2016',
     'type': 'Home',
     'purpose': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been th',
     'due_date': '02/september/2018'},
    {'id': 2,
     'name': 'Meet Peter',
     'date_created': '24/Aug/2016',
     'type': 'Sports',
     'purpose': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been th',
     'due_date': '02/september/2018'},
]

# A route to modify an entry.
@app.route('/api/v1/resources/entries/modify/<string:name>',methods=['PUT'])
def modifyentry(name):
    entrynew =[entry for entry in entries if entry['name'] == name]
    entrynew[0]['name'] = request.JSON['name']
    return jsonify({'entry' : entrynew[0] })

# A route to fetch all entries.
@app.route('/api/v1/resources/entries/all', methods=['GET'])
def api_all():
    return jsonify(entries)

# A route to fetch a single entry.
@app.route('/api/v1/resources/entries', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])

    elif 'id' not in request.args:
        id = int(request.args['id'])
        return make_response(jsonify({"result": "No existing entry with that id"})), 200
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for entry in entries:
        if entry['id'] == id:
            results.append(entry)
        # elif entry['id']!=id:
        #     return make_response(jsonify({"result": "No existing entry with that id"})), 200

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/api/v1/resources/create', methods=['GET', 'POST']) #allow both GET and POST requests
def api_postentry():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        name = request.form.get('name')
        datecreated = request.form['datecreated']
        entry_type = request.form['entry_type']
        purpose = request.form['purpose']
        duedate = request.form['duedate']

        return jsonify('''<h1>The Entry Name is: {}</h1>
                  <h1>The Entry Date Created is: {}</h1>
                  <h1>The Entry Type is: {}</h1>
                  <h1>The Entry Purpose is: {}</h1>
                  <h1>The Entry Due Date is: {}</h1>'''.format(name, datecreated,entry_type,purpose,duedate))

    return '''<form method="POST" center>
                <h3>Enter Diary details<h3><br>
                  Name: <input type="text" name="name"><br><br>
                  Date Created: <input type="text" name="datecreated"><br><br>
                  Type: <select name="entry_type"><option value="">Choose...</option>
                        <option value="office">Office</option>
                        <option value="home">Home</option>
                        <option value="sport">Sports</option>
                        </select><br><br>
                  Purpose: <input type="text" name="purpose"><br><br>
                  Due Date: <input type="text" name="duedate"><br><br>
                  <input type="submit" value="Submit"><br>
              </form>'''
