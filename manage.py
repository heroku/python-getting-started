import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
employees = [
    {'ecode': '056964',
     'name': 'mekala',
     'password': 'Jesila@21',
     'designation': 'DM',
     'doj': '2019'},
    {'ecode': '056965',
     'name': 'kala',
     'password': 'Jesi@21',
     'designation': 'DM',
     'doj': '2018'},
    {'ecode': '056966',
     'name': 'meka',
     'password': 'sila@21',
     'designation': 'DM',
     'doj': '2017'}
]


@app.route('/', methods=['GET'])
def home():
    return '''<h1>employee-details</h1>
<p>A prototype API for employee detail of TVS.</p>'''


@app.route('/api/employee-details', methods=['GET'])
def api_all():
    return jsonify(employees)


@app.route('/api/employee-details', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'ecode' in request.args:
        id = int(request.args['ecode'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for employee in employees:
        if employee['ecode'] == id:
            results.append(employee)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()
