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
 export FLASK_APP=wsgi/flaskapp.py
 flask run


** TEST
using PyTest: https://docs.pytest.org/en/latest/
http://pytest.readthedocs.io/en/latest/goodpractices.html

from the project root, run pytest


** CONFIGURATION
https://martin-thoma.com/configuration-files-in-python/
https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b


** PYTHONANYWHERE
Steps here: https://help.pythonanywhere.com/pages/Flask/

Copy the project
 Open a shell
 git clone https://github.com/rainbowbreeze/yellowbutler.git/ yellowbutler
 cd yellowbutler/bot/src
 mkvirtualenv --python=/usr/bin/python3.6 yellowbutler-venv
 pip install -r requirements.txt
 (virtualenv created under /home/yellowbutler/.virtualenvs/yellowbutler-venv, as per command output)
 
Create a new webapp
 Select Manual mode, python 3.6 and confirm everything
 virtualenv:  /home/yellowbutler/.virtualenvs/yellowbutler-venv
 change WSGI file adding under the section +++++++++++ FLASK +++++++++++
 
  import sys
  path = '/home/yellowbutler/yellowbutler/bot/src'
  if path not in sys.path:
      sys.path.append(path)
  from wsgi.flaskapp import app as application

if I put the path to the wsgi folder, /home/yellowbutler/yellowbutler/bot/src/wsgi, I obtain a
 ModuleNotFoundError: No module named 'yellowbot'
because the root is not anymore src, but becomes src/wsgi, and so all the python import fails


To test:
curl -X POST https://yellowbutler.pythonanywhere.com/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Ciao da meeeeee\"}}"
(remember to authorize the key in the config file, and reload the webapp)
