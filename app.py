from App.views import app

from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True, port=3000)