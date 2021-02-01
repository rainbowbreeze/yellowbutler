# Deprecated - Deploy Under PythonAnaywhere

Steps here: https://help.pythonanywhere.com/pages/Flask/

Copy the project
Open a shell
```
git clone https://github.com/rainbowbreeze/yellowbutler.git/ yellowbutler
cd yellowbutler/bot/src
mkvirtualenv --python=/usr/bin/python3.6 yellowbutler-venv
```
later or, to activate the virtual env: workon yellowbutler-venv

```
pip install -r requirements.txt
```
(virtualenv created under /home/yellowbutler/.virtualenvs/yellowbutler-venv, as per command output)
 
Create a new webapp
- Select Manual mode, python 3.6 and confirm everything
- virtualenv:  /home/yellowbutler/.virtualenvs/yellowbutler-venv
- change WSGI file adding under the section +++++++++++ FLASK +++++++++++
```
import sys
path = '/home/yellowbutler/yellowbutler/bot/src'
if path not in sys.path:
    sys.path.append(path)
from wsgi.flaskapp import app as application
```

If I put the path to the wsgi folder, /home/yellowbutler/yellowbutler/bot/src/wsgi, I obtain a
 ModuleNotFoundError: No module named 'yellowbot'
because the root is not anymore src, but becomes src/wsgi, and so all the python import fails

To test:
```
curl -X POST https://yellowbutler.pythonanywhere.com/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Ciao da meeeeee\"}}"
```
(remember to authorize the key in the config file, and reload the webapp)