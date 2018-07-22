from flask import Flask, request, jsonify, make_response, render_template
app = Flask(__name__)


@app.route('/contacts', methods=['GET', 'POST', 'DELETE', 'PUT'])
def contacts():
    if request == 'GET':
        return make_response(jsonify({"result": "coming soon"})), 200
    elif request.method:
        return make_response(jsonify({"result": "Post Done"})), 200
        # pass


@app.route('/profile/<username>')
def profile(username):
    return 'Hello there %s' % username


@app.route('/user/<int:post_id>')
def showint(post_id):
    return 'Hey There, your POST ID is %s' % post_id


@app.route('/welcome')
def welcome():
    return render_template('index.html')  # render a template


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


if __name__ == '__main__':
    app.run(debug=True, port=3000)