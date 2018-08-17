** CREATE THE ENVIRONMENT

** PYCHARM



https://docs.python.org/3/library/venv.html
python3 -m venv venv
(last venv is the venv name)

source venv/bin/activate
deactivate

pip install  -r requirements.txt

To configure inside PyCharm, I first create a venv for the new project, selecting the python interpreter in brew.
Alternatively, create the venv in Pycharm, then from command line remove it and create a new one using python3 and rename the venv in the project preferences


** LINUX INSTALL
sudo snap install gcloud


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


** APPENGINE
https://cloud.google.com/appengine/docs/flexible/python/quickstart

https://console.cloud.google.com/projectselector/appengine/create?lang=flex_python&st=true&_ga=2.125561612.704564983.1514577758-1153595002.1514577758
create project yellowbutler

Copy the project
 Open a CloudShell
   rainbowbreeze_dev@yellowbutler-190521
   /home/rainbowbreeze_dev
 git clone https://github.com/rainbowbreeze/yellowbutler.git/ yellowbutler
 cd yellowbutler/bot/src
 virtualenv --python=python3.4 venv
 source venv/bin/activate
 pip install -r requirements.txt
 
Test the app
 export FLASK_APP=wsgi/flaskapp.py
 flask run
 (if run with python wsgi/flaskapp.py, it doesn't work)

Deploy the app
 Changed app.yaml adding the right module name, using dotted notation
  entrypoint: gunicorn -b :$PORT wsgi.flaskapp:app
 added gunicorn to requirements.txt and rerun 
 gcloud app deploy -v [YOUR_VERSION_ID]
 fingers crossed
 gcloud app browse
 To see logs in the Cloud Console: https://console.cloud.google.com/gcr/builds/adf5a006-f112-4dc4-9d59-86ed1d99b37b?project=yellowbutler-190521
(gcloud app deploy -v 1 --quit)


To deploy from local machine

gcloud config configurations list
 to check the active configuration and the list of configurations
gcloud init
 and select to create a new configuration to connect a new account to the project id
once finished the usual command to deploy the app
gcloud app deploy -v 1 --quiet

gcloud config configurations activate yellowbot
 to switch among configurations

Reference: https://www.the-swamp.info/blog/configuring-gcloud-multiple-projects/


** SCHEDULER
Create a cron.yaml following https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml
gcloud app deploy cron.yaml --verbosity debug --quiet

 

** DEPLOY UNDER PYTHONANYWHERE

Steps here: https://help.pythonanywhere.com/pages/Flask/

Copy the project
 Open a shell
 git clone https://github.com/rainbowbreeze/yellowbutler.git/ yellowbutler
 cd yellowbutler/bot/src
 mkvirtualenv --python=/usr/bin/python3.6 yellowbutler-venv
  later or, to activate the virtual env: workon yellowbutler-venv

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

LOGGING Under PAW
 https://www.pythonanywhere.com/forums/topic/3120/
  print('debug info', file=sys.stderr)
  end up in /var/log/…error.log (in some time after request)
  
  
DAMN!!!
https://help.pythonanywhere.com/pages/403ForbiddenError/
https://www.pythonanywhere.com/whitelist/
PythonAnywhere is a no way choice, unfortunately :(