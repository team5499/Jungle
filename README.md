# Jungle
A lightweight, websockets based dashboard. Built using [Flask](http://flask.pocoo.org/).

The goal of this project is to build a smart dashboard that is extremely lightweight, easy to implement, and easy to use.

## conf.json
This file is used to configure the different available pages on the dashboard.

## Development
To set up the development environment, run `gradle install_hooks`. In order to start the dev server, simply run `gradle run`. This tells the server to load the page configuration from `resources/conf.json`, to host the server on the local machine, and to use port `5800`. To view the dashboard, navigate to `localhost:5800` in any web browser. NOTE: at competitions, only ports `5800` through `5810` are open for teams to use on the field. This is why the server is hosted on port `5800`.

After cloning, make sure to run `gradle install_hooks`.

## Documentation Todo
- How to create new widgets
    - How to write settings forms
    - How the configuration file is structured
- How to install on the robot, and integrate with the robot code
- How to setup environment for building XARs

## Dev Notes

NOTE: when implementing this dashboard, make sure that the `conf` file is modifiable. Also, make sure `dashboard/main.py` is executable.
