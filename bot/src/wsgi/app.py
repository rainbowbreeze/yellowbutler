#!flask/bin/python
from flask import Flask

app = Flask(__name__)

from yellowbot.yellowbot import YellowBot

@app.route('/')
def index():
    yb = YellowBot()
    # return yb.echo_message("Ciao")
    return yb.process_intent("trace_music", "bella storia")


if __name__ == '__main__':
    app.run(debug=True)
