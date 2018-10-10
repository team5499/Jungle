# Jungle
A lightweight, websockets based dashboard. Built using Flask.

The goal of this project is to build a smart dashboard that is extremely lightweight, easy to implement, and easy to use.

## conf.json
This file is used to configure the different available pages on the dashboard.

## vars.json
This file is used to store the variables that the dashboard makes available. If the `writable` field is `true`, the variable is considered writable, meaning that when the variable is changed on the dashboard, it is immediately written to the file. The variable will be initialized with whatever value the `value` field contains. If the `writable` field is `false`, the variable is considered read only. When the value is changed on the dashboard, it updates for all clients, but the value is not saved to the file. In this case, the `value` field is used to initialize the variable. Read only variables are useful when you want to have a value that is going to change rapidly, but that doesn't need to be recorded. It also frees up the system disk usage, since the value isn't being written every time it changes.

## Development
To set up the development environment, run `pip3 install -r requirements-minimal.txt` and `pip3 install -r requirements-dev-minimal.txt`. This will install the required libraries to run the dev server. In order to start the dev server, make sure that `main.py` is executable, and run `./main.py -c conf.json -v vars.json -a 127.0.0.1 -p 5800 -d`. This tells the server to load the page configuration from `conf.json`, the variable configuration from `vars.json`, to host the server on the local machine, and to use port 5800. The `-d` flag tells the server to run in development mode. After starting the server, navigate to `localhost:5800` in any web browser. NOTE: at competitions, only ports 5800 through 5810 are open for teams to use on the field.

Before committing changes, make sure to run the pre-commit hook by executing `make test`. To install the hooks, run `make install-hooks`. To upgrade requirements, run `make upgrade-requirements`.

## Documentation Todo
- How to create new widgets
    - How to write settings forms
    - How the configuration file is structured
- How to install on the robot, and integrate with the robot code

## Dev Notes

NOTE: when implementing this dashboard, make sure that the `conf` and `vars` file are both modifiable. If they are not, use chmod to change the file permissions.
