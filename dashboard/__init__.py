import argparse
import os
from dashboard.main import main


def start():
    print(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', required=False, default='/home/lvuser/dashboard/conf.json',
                        help='the path to the configuration file')
    parser.add_argument('-v', '--vars', required=False, default='/home/lvuser/dashboard/vars.json',
                        help='the path to the variable file')
    parser.add_argument('-a', '--addr', required=False, default='0.0.0.0',
                        help='the host address for the dashboard server')
    parser.add_argument('-p', '--port', required=False, default=5800,
                        help='the port to host the dashboard from (for the FMS, host on port 5800 to 5810')
    parser.add_argument('-d', '--debug', required=False, default=False,
                        help='launch the server in debug mode', action='store_true')

    kwargs = vars(parser.parse_args())
    main(**kwargs)
