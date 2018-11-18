#!/usr/bin/env python3.6
import signal
import argparse

from dashboard import Dashboard

def main(addr, port, conf, team):
    dashboard = Dashboard(addr, port, conf, team)

    def interrupt_handler(sig, frame):
        print('shutting down...')
        dashboard.stop()
        exit(0)
    signal.signal(signal.SIGINT, interrupt_handler)
    dashboard.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--conf', required=False, default="conf.json",
                        help='the path to the configuration file')
    parser.add_argument('-a', '--addr', required=False, default="0.0.0.0",
                        help='the host address for the dashboard server')
    parser.add_argument('-p', '--port', required=False, default=5800,
                        help='the port to host the server from (must be between 5800 and 5810)')
    parser.add_argument('-t', '--team', required=True,
                        help='your team number')

    args = parser.parse_args()
    main(args.addr, args.port, args.conf, args.team)
