from flask import Flask

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py


@app.route("/")
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run()
