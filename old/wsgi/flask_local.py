"""
Conventions:
 Base APIs are exposed using the address https://_hostname_/yellowbutler/api/v1.0/
 
 Authorization code is passed in the X-Authorization field of the payload (or headers)
"""
from flask import Flask, request

# Added to prevent ImportError: No module named 'yellowbutler'
import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
# ---

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


if __name__ == "__main__":
    app.run()
