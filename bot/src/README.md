** CREATE THE ENVIRONMENT

Install python 3.7 in Linux or in MacOS with brew
git clone https://github.com/rainbowbreeze/yellowbutler.git master
cd bot/src

From https://docs.python.org/3/library/venv.html
python3 -m venv venv
(last venv is the venv name)

source venv/bin/activate
pip install -r requirements.txt
deactivate


* PYCHARM 2018.2 CONFIG

File -> New Project
  Location bot/src
  Project Interpreter
    New environment using: Virtualenv
    Location: bot/src/venv
    Base interpreter: python 3.7
PyCharm creates global virtualenv by default, so rename the venv folder with something else, create the project, then rename back venv folder.
File -> Settings
  Project Interpreter
    Select the venv just created under the project folder
Everything should work under Python in this way


** RUN

from CL
  export FLASK_APP=wsgi/flaskapp.py
  flask run
  (if run with python wsgi/flaskapp.py, it doesn't work)
from PyCharm
  go to wsgi/flaskapp.py and run it. If there is an error with config file, read under the wrong directory, edit the run configuration and set bot/src as working path


** TEST
using PyTest: https://docs.pytest.org/en/latest/
http://pytest.readthedocs.io/en/latest/goodpractices.html

from the project root, run pytest


** CONFIGURATION
https://martin-thoma.com/configuration-files-in-python/
https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b






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


** APPENGINE

* LINUX INSTALL
sudo snap install gcloud
gcloud auth login
gcloud config set project PROJECT_ID
gcloud app deploy
  gcloud topic gcloudignore


* GAE Standard python 3.7
https://cloud.google.com/appengine/docs/standard/python3
https://cloud.google.com/appengine/docs/standard/python3/building-app
Create a new AppEngine project and enable billing, otherwise deploy won't work.
No need to vendoring libraries, they're added using requirements.txt file in the project root
Logging: gcloud app logs tail -s default


* Cloud Shell
 Open a CloudShell from the project
   rainbowbreeze_dev@yellowbutler-213621
   /home/rainbowbreeze_dev
 git clone https://github.com/rainbowbreeze/yellowbutler.git/ yellowbutler
 cd yellowbutler/bot/src
 virtualenv --python=python3.7 venv
 source venv/bin/activate
 pip install -r requirements.txt
 
Deploy the app
  https://cloud.google.com/appengine/docs/standard/python3/runtime?hl=sl#application_startup
  Changed app.yaml adding the right module name, using dotted notation
    entrypoint: gunicorn -b :$PORT wsgi.flaskapp:app
    added gunicorn to requirements.txt and rerun 
  gcloud app deploy -v [YOUR_VERSION_ID]
  gcloud app deploy -v 1 --quiet
  gcloud app browse

To see logs in the Cloud Console: https://console.cloud.google.com/logs/viewer?project=yellowbutler-213621

Run locally as in GAE
gunicorn -b :8080 wsgi.flaskapp:app



To check gcloud configurations
https://www.the-swamp.info/blog/configuring-gcloud-multiple-projects/
gcloud config configurations list
 to check the active configuration and the list of configurations
gcloud init
 and select to create a new configuration to connect a new account to the project id
once finished the usual command to deploy the app
gcloud app deploy -v 1 --quiet

gcloud config configurations activate yellowbot
 to switch among configurations


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