** CREATE THE ENVIRONMENT

https://docs.python.org/3/library/venv.html
python3 -m venv venv
(last venv is the venv name)

source venv/bin/activate
deactivate

To configure inside PyCharm, I first create a venv for the new project, selecting the python interpreter in brew.
Alternatively, create the venv in Pycharm, then from command line remove it and create a new one using python3 and rename the venv in the project preferences


** FLASK
create folder wsgi, as source folder
pip install flask
added flask to requirements.txt
create app.py under wsgi
---
#!flask/bin/python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
---

from PyCharm, click on app.py and "Run app"
from CL
 export FLASK_APP=wsgi/app.py
 flask run


** TEST
using PyTest: https://docs.pytest.org/en/latest/
http://pytest.readthedocs.io/en/latest/goodpractices.html

from the project root, run pytest