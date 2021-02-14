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
```
Note: _Updating and removing components using gcloud components is disabled if you installed Cloud SDK using apt-get or yum. To manage the Cloud SDK in this case, continue using the package management tool used during installation._

To use the local development server in App Engine, also the datastore emulator has to be installed:
```
sudo apt-get install google-cloud-sdk-datastore-emulator
```


## Google Cloud SDK project initialization
[Initialize](https://cloud.google.com/sdk/docs/initializing) the gcloud environment and get started:
```
gcloud init
```
gcloud init --console-only to avoid browser login
It's important to pick-up the right [location](https://cloud.google.com/appengine/docs/locations) for the project


or, if a user has already been configured:
```
gcloud auth login
gcloud config set project PROJECT_ID
```
It's important to remember the PROJECT_ID, it's used in the YellowBot config files.


### Google Cloud SDK authentication
Google App Engine supports several [ways to store data](https://cloud.google.com/appengine/docs/standard/python3/storage-options). YellowBot uses Cloud Datastore, via the Google Cloud SDK. In order to run YellowBot both on App Engine and locally, (access private data on behalf of a service account outside Google Cloud environments) it's necessary to create a [service accout with User-managed keys](https://cloud.google.com/iam/docs/service-accounts#user-managed_keys), and use it with the Google Cloud SDK authentication. If the idea is to run it only on GCP, it's more secure to use the Google-managed keys, or switch to a Environment-provided service account.
Details on the [different types of authentication available](https://cloud.google.com/docs/authentication). 

[Create and authenticate as a service account](https://cloud.google.com/docs/authentication/production#auth-cloud-explicit-python)
- In the Cloud Console, go to the [Service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts) page.
- Go to the Create Service Account Key page
- From the Service account list, select New service account.
- In the Service account name field, enter a name.
- From the Role list, select "App Engine default service account" (it should be enough to access datastore)
- Click Create. A JSON file that contains your key downloads to your computer.
- Put this file under bot/src folder with the name service_account.json (defaul convention of the Google Cloud SDK)

Deprecated - use a User accounts to access the resources while running YellowBot locally (not suggested, and it won't work once deployed to GAE - more on what is does and what it's a non best-security practice [here](https://www.bernardorodrigues.org/post/bypass-app-engine-auth-local))
```
gcloud auth application-default login
```

### Configure Firestore in Datastore mode
[Tutorial](https://cloud.google.com/appengine/docs/standard/python3/using-cloud-datastore)
Firestore in Datastore mode has [free quota too](https://cloud.google.com/datastore/pricing)



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

To quit from the environment
```
deactivate
```


### VSCode setup
Create the basic environment
https://code.visualstudio.com/docs/python/tutorial-flask

Enable tests
https://code.visualstudio.com/docs/python/testing

Optional- Install [PyLance](https://devblogs.microsoft.com/python/announcing-pylance-fast-feature-rich-language-support-for-python-in-visual-studio-code/) for a better Python support.  
If PyLance will report error in missing imports for local libraries, it is because it starts to process from the project root folder. [See issue](https://github.com/microsoft/pylance-release/issues/519). To solve, follow the [Unresolved import warnings](https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md#unresolved-import-warnings) and add this line to the .vscode/setting.json on the root folder
```
{
    "python.analysis.extraPaths": ["./bot/src"]
}
```



## Configuring gears
YellowBot works using the concept of gears. Each gear offers a functionality. So there is a weather gear for weather forecasting, and echo gear for sending a message to a specific surface (Telegram), a youtube video gears for getting the latest videos published on a channel, etc.
The majority of gears requires parameters to work, like API keys, telegram chat id, etc. There paramenters are configured via a specific config file

### Edit configuration
```
cp yellowbot_config_template.json yellowbot_config.json
cp yellowbot_tasks_template.json yellowbot_tasks.json
```
Then, edit files accordingly to the comments.

### Weather gear
TBD

## Telegram gear
TBD

### YouTube gear
Enable YoutTube API for the current GCP project and obtain a YouTube API key following [these instructions](https://developers.google.com/youtube/v3/getting-started)
Check for [API quota](https://console.developers.google.com/iam-admin/quotas) used.

### Telegram Support
In order to communicate with the external world, YellowBot needs at least one surface. Telegram is the default surface, and in order to configure it, a bot key and a chat_id are required. There are many tutorials and guides that walk thru the process.
Once configured the bot, add these options to activate quick commands in Telegram interface
checkfornews - Check news from various sources



## Run YellowBot locally
Assuming working directory is bot/src - this is important for module's relative paths, configuration path, etc.
The different ways to launch the app are in the [official reference](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app).

### From CL, as normal python app
Run locally the app launching the python script that starts flask environment. _(dir is bot/scr, with venv activated)_
```
FLASK_APP=wsgi/flaskapp.py flask run
```
Alternatively:
```
export FLASK_APP=wsgi/flaskapp.py
flask run
```
_(if run with python wsgi/flaskapp.py, it doesn't work)_

Test if everything works with: 
```
curl -X POST http://127.0.0.1:5000/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Hello world\"}}"
```

### From CL, as a GAE app
To simulate a production App Engine environment, you can run the full Web Server Gateway Interface (WSGI) server locally. To do this, use the same command specified as entrypoint in your app.yaml, for example:
```
gunicorn -b :5000 wsgi.flaskapp:app
```
Test with: 
```
curl -X POST http://127.0.0.1:5000/yellowbot/api/v1.0/intent -H "X-Authorization:authorized_key_1" -H "Content-Type: application/json" -d "{\"intent\":\"echo_message\", \"params\":{\"message\":\"Hello world\"}}"
```

There is also the option to use the [local development server](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app#local-dev-server), dev_appserver.py - this is useful to emulate an application running in production, and potentially also emulate services like Cloud Datastore, Cloud Bigtable and Cloud Pub/Sub locally. More on the dev-oriented [README.md](src/README.md)



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

It's possible to use .gcloudignore file to specify files and directories that will not be uploaded to App Engine when the app is deployed.


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

Get information on the current App Engine app, location included (it's possible to omit the project id)
```
gcloud app describe --project <projectId>
```

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
