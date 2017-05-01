from flask import Flask

# Added to prevent ImportError: No module named 'yellowbutler'
import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
# ---

from yellowbutler.yellowbutler import YellowButler


app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

yellowbutler = YellowButler()


@app.route("/")
def hello_world():
    # return 'Hello World!'
    return yellowbutler.get_message()


if __name__ == "__main__":
    app.run()
