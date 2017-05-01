from flask import Flask
from yellowbutler.yellowbutler import YellowButler

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

yellowbutler = YellowButler()


@app.route("/")
def hello_world():
    # return 'Hello World!'
    return yellowbutler.get_message()

# As per PythonAnywhere documentation, "you should make sure your code
# does *not* invoke the flask development server with app.run(), as it
# will prevent your wsgi file from working.
