# Jungle
A lightweight, websockets based dashboard. Built using Flask.

The goal of this project is to build a smart dashboard that is extremely lightweight, easy to implement, and easy to use.


NOTE: when implementing this dashboard, make sure that the `conf` and `vars` file are both modifiable. If they are not, use chmod to change the file permissions.

## conf.json
This file is used to configure the different available pages on the dashboard.

## vars.json
This file is used to store the variables that the dashboard makes available. If the `writable` field is `true`, the variable is considered writable, meaning that when the variable is changed on the dashboard, it is immediately written to the file. The variable will be initialized with whatever value the `value` field contains. If the `writable` field is `false`, the variable is considered read only. When the value is changed on the dashboard, it updates for all clients, but the value is not saved to the file. In this case, the `value` field is used to initialize the variable. Read only variables are useful when you want to have a value that is going to change rapidly, but that doesn't need to be recorded. It also frees up the system disk usage, since the value isn't being written every time it changes.

## How to add a new page


## Documentation Todo
- How to create new widgets
    - How to write settings forms
    - How the configuration file is structured
- How to install on the robot, and integrate with the robot code
