# YELLOW BOT
The main YellowButler project component, a bot running on GAE Standard


## Environment setup with Google App Engine and Linux

YellowBot runs on [App Engine Standard environment](https://cloud.google.com/appengine/docs/the-appengine-environments). As for [Jan 2021](https://cloud.google.com/appengine/quotas), _The App Engine standard environment gives you 1 GB of data storage and traffic for free, which can be increased by enabling paid applications. However, some features impose limits unrelated to quotas to protect the stability of the system_

Some tutorials:
- Official [App Engine Python tutorials](https://cloud.google.com/appengine/docs/standard/python3), with quickstart.


### Google Cloud SDK Linux install
[Install Cloud SDK on Ubuntu](https://cloud.google.com/sdk/docs/quickstart#deb). It cannot be installed via [snap package](https://cloud.google.com/sdk/docs/downloads-snap), because the package miss the appengine-python module.
```
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get install apt-transport-https ca-certificates gnupg
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-sdk
sudo apt-get install google-cloud-sdk-app-engine-python google-cloud-sdk-app-engine-python-extras
sudo apt-get install google-cloud-sdk-datastore-emulator
```
Note: _Updating and removing components using gcloud components is disabled if you installed Cloud SDK using apt-get or yum. To manage the Cloud SDK in this case, continue using the package management tool used during installation._

[Initialize](https://cloud.google.com/sdk/docs/initializing) the gcloud environment and get started:
```
gcloud init
```
gcloud init --console-only to avoid browser login

or, if a user has already been configured:
```
gcloud auth login
gcloud config set project PROJECT_ID
```

To enable Google Cloud SDK authentication
```
gcloud auth application-default login
```
TODO: enable service account via https://cloud.google.com/docs/authentication


### Python installation and environment setup

Install python 3.x in Linux or in MacOS with brew

Download the application
```
git clone https://github.com/rainbowbreeze/yellowbutler.git master
cd bot/src
```

Create the [Python virtual environment](https://docs.python.org/3/library/venv.html) and activate it
```
python3 -m venv venv
```
_(last venv is the venv name)_

```
source venv/bin/activate
pip install -r requirements.txt
```

To quick from the environment
```
deactivate
```


### VSCode setup
Create the basic environment
https://code.visualstudio.com/docs/python/tutorial-flask

Enable tests
https://code.visualstudio.com/docs/python/testing



## Run YellowBot locally
Assuming working directory is bot/src - this is important for module's relative paths, configuration path, etc

### Edit configuration
```
cp yellowbot_config_template.json yellowbot_config.json
cp yellowbot_tasks_template.json yellowbot_tasks.json
```
Then, edit files accordingly to the comments.


### From CL, as normal python app
As per [official reference](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app), it's possible to run locally the app launching the python script that starts flask environment
_(dir is bot/scr, with venv activated)_
```
FLASK_APP=wsgi/flaskapp.py flask run
```
alternatively:
```
export FLASK_APP=wsgi/flaskapp.py
flask run
```
_(if run with python wsgi/flaskapp.py, it doesn't work)_

Test with: 
```
curl -X POST http://127.0.0.1:5000/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Hello world!\"}}"
```

### From CL, as a GAE app
To simulate a production App Engine environment, you can run the full Web Server Gateway Interface (WSGI) server locally. To do this, use the same command specified as entrypoint in your app.yaml, for example:
```
gunicorn -b :5000 wsgi.flaskapp:app
```
Test with: 
```
curl -X POST http://127.0.0.1:5000/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Hello world!\"}}"
```

There is also the option to use the [local development server](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app#local-dev-server), dev_appserver.py - this is useful to emulate services like Cloud Datastore, Cloud Bigtable and Cloud Pub/Sub. Unfortunately, [offical docs](https://cloud.google.com/appengine/docs/standard/python/migrate-to-python3/testing#testing-on-app-engine) says: _The [local development server](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app#local-dev-server) that is included in the Cloud SDK is available in alpha for Python 3 apps. We recommend you use standard Python 3 tools instead of this local development server._



### From VSCode
- Once configured the IDE, simply CTRL+F5 or Debug -> Run without debugger. or select the arrow in the "Debug" left panel section



## Deploy YellowBot

### From CL
```
gcloud app deploy -v 1 --quiet
```

To open the browser at the current app's page:
```
gcloud app browse
```

To see logs in the Cloud Console use the link https://console.cloud.google.com/logs/viewer?project=%YOUR_PROJECT_ID%
from Cloud Shell or local
```
gcloud app logs tail -s default 
```



### Using Google Cloud Shell
Open a CloudShell from the project
```
git clone https://github.com/rainbowbreeze/yellowbutler.git/ yellowbutler
cd yellowbutler/bot/src
virtualenv --python=python3.7 venv
source venv/bin/activate
pip install -r requirements.txt
``` 

Deploy the app [guide](https://cloud.google.com/appengine/docs/standard/python3/runtime?hl=sl#application_startup)
```
gcloud app deploy -v [YOUR_VERSION_ID]
gcloud app deploy -v 1 --quiet
```



## Appendix

### Misc GAE commands

How to check for [gcloud configurations](https://www.the-swamp.info/blog/configuring-gcloud-multiple-projects/):

Create a new configuration to connect a new account to the project id
```
gcloud init
``` 
Check the active configuration and the list of configurations
```
gcloud config configurations list
```

To switch among configurations
```
gcloud config configurations activate yellowbot
```

To change gcloud user:
```
gcloud config set account ACCOUNT
```

Check installed components with:
```
gcloud components list
```
