from flask import Flask, request
from yellowbutler.yellowbutler import YellowButler

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

yellowbutler = YellowButler()

# Basic address for all the API calls
BASIC_ADDRESS = '/yellowbutler/api/v1.0'

@app.route("/")
def hello_world():
    return 'Hello World!'


@app.route('{}/message'.format(BASIC_ADDRESS), methods=['POST'])
def echo_message():
    print('***************************')
    print(request.headers)
    print('***************************')
    print(request)
    print('***************************')
    print(request.get_json())
    print('***************************')
    return yellowbutler.echo_message('AAAA', 'Welcome to the world!')


def extract_auth(response):
    """Extracts auth header from the call"""
    pass

# As per PythonAnywhere documentation, "you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.
