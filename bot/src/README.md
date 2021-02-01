# YELLOWBOT GAE AND PYTHON SPECIFIC CONFIGURATIONS

## Run YellowBot

from CL
  export FLASK_APP=wsgi/flaskapp.py
  flask run
  (alternatively: FLASK_APP=wsgi/flaskapp.py flask run)
  (if run with python wsgi/flaskapp.py, it doesn't work)
from VSCode
  Once configured the IDE, simply CTRL+F5 or Debug -> Run without debugger. or select the arrow in the "Debug" left panel section
from PyCharm
  go to wsgi/flaskapp.py and run it. If there is an error with config file, read under the wrong directory, edit the run configuration and set bot/src as working path



## Run tests
using PyTest: https://docs.pytest.org/en/latest/
http://pytest.readthedocs.io/en/latest/goodpractices.html

from the project root
```
pytest
```


## CONFIGURATION
https://martin-thoma.com/configuration-files-in-python/
https://hackernoon.com/4-ways-to-manage-the-configuration-in-python-4623049e841b


** REQUIREMENTS
pip freeze > requirements.txt
pip install -r requirements.txt


## FLASK
create folder wsgi, as source folder
pip install flask
added flask to requirements.txt
create app.py under wsgi
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




## SCHEDULER
Create a cron.yaml following
https://cloud.google.com/appengine/docs/flexible/python/scheduling-jobs-with-cron-yaml
or
https://cloud.google.com/appengine/docs/standard/python/config/cron
gcloud app deploy cron.yaml --verbosity debug --quiet
Check for log on Cloud console: https://console.cloud.google.com/appengine/taskqueues/cron
 

Changed app.yaml adding the right module name, using dotted notation
```
entrypoint: gunicorn -b :$PORT wsgi.flaskapp:app
```

Added gunicorn to requirements.txt and rerun 
