# YELLOWBOT GAE AND PYTHON SPECIFIC CONFIGURATIONS


## Python notes

## Run tests
using PyTest: https://docs.pytest.org/en/latest/
http://pytest.readthedocs.io/en/latest/goodpractices.html

from bot/src folder
```
pytest
```

### Manage configurations
https://martin-thoma.com/configuration-files-in-python/
https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b

I put in the configuration class logic to obtain the file both via a relative path (relative to the root folder when the python is lauched), and also looking inside of the folder where the specific class is, as fallback. This is particuarly useful with tests, so I can pass different configuration files while running tests.


### PIP management
```
pip freeze > requirements.txt
pip install -r requirements.txt
```


### Flask
```
pip install flask
```
Add flask to requirements.txt

To put all Flask logic in a specific place, separated from the main app logic, create a folder wsgi, as source folder.
Then, create app.py under wsgi folder
```
#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
```

and run the app with
```
FLASK_APP=wsgi/flaskapp.py flask run
```


## App Engine notes

### Scheduler
Create a cron.yaml following
https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml
or
https://cloud.google.com/appengine/docs/standard/python/config/cron

To deploy new tasks, without redeploying the whole app:
```
gcloud app deploy cron.yaml --verbosity debug --quiet
```
Check for log on Cloud console: https://console.cloud.google.com/appengine/taskqueues/cron


### Flask and App Engine local runtime
Changed app.yaml adding the right module name, using dotted notation
```
entrypoint: gunicorn -b :$PORT wsgi.flaskapp:app
```

Added gunicorn to requirements.txt, so App Engine can be launched locally
