
"# slot_race_track" 

The code for the digital twin (in Godot) is available on this Github.

The code for the virtual simulation of the racetrack is also available on this Github, and is named Server_Pi.py

To allow communication between Server_Pi.py and Godot make sure to:
1. Open Server_Pi.py
2. Open the Godot project in Godot (2D navigation demo)
3. Run the python file (Server_Pi.py)
4. Start the Godot game


# Pipenv
To make it easier to install all the required packages for the slot race track project, a pipenv
environment has been made. See below on how to make sure you install the virtual environment
properly.

## requirements
- Pip installed (should be included in the Python installation)
- Pipenv package is installed: `pip install pipenv`

## Installing the virtual environment
To install the pipenv environment, the following command needs to be executed in a command line:
- `pipenv install`

To access the virtual environment and see the installed packages, the following command is used:
- `pipenv shell`

To see which packages are installed, the following command is used:
- `pip list`

After executing the `pipenv shell` command, the python files can now be executed within the virtual
environment. Simply run them like you normally would run a python file. for example:
- `python Server_Pi.py`

## IDE interpreter
When using an IDE to run your Python files, make sure you change the interpreter to the
virtual environment. When using a different IDE as described below, please add the steps on how to
do this.

### VS Code
Assuming the Python extension has already been installed:
1. Press `f1` key
1. Type `Python: Select Interpreter` and select the option
1. Select the SlotRacer virtual environment in the list
1. When running code, Select `Run Python File in Terminal` (you may need to reload the VS code
   window first)
