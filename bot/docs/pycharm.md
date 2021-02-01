# Deprecated - PyCharm 2018.2 setup


## PyCharm setup
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

## Running the app
go to wsgi/flaskapp.py and run it. If there is an error with config file, read under the wrong directory, edit the run configuration and set bot/src as working path

