#!/usr/bin/env python3
import time
import threading
import argparse
import signal
from flask import Flask, render_template, current_app, redirect, abort
from flask_socketio import SocketIO, emit, join_room

from var_handler import VariableHandler
from conf_handler import ConfigurationHandler

class Dashboard():
    """This is the main web application class"""
    app = Flask(__name__)
    sio = SocketIO(app, async_mode="eventlet")

    def __init__(self, conf_path, var_path, address="127.0.0.1", port=5800, team_number=5499, debug=False):
        with Dashboard.app.app_context():
            current_app.web_instance = self

        self.team_number = team_number
        self.var_handle = VariableHandler(file_path=var_path)
        self.conf_handler = ConfigurationHandler(file_path=conf_path)

        self.address = address
        self.port = port
        self.debug = debug
        # self.thread = threading.Thread(target=Dashboard._server_thread, args=[address, port, debug], name="Dashboard Server", daemon=True)

    def start(self):
        Dashboard._server_thread(self.address, self.port, self.debug)

    def stop(self):
        pass

    ### WEB PAGES ###
    
    @staticmethod
    @app.route("/")
    def index():
        """Redirect the client to the `drive` page"""
        return redirect(f"/drive")

    @staticmethod
    @app.route("/favicon.ico")
    def favicon():
        """Handle favicon request for redirect page"""
        return None

    @staticmethod
    @app.route("/<page>")
    def load_page(page=None):
        if not page in Dashboard.get_page_ids():
            abort(404)
        return render_template(
            f"layout.html", 
            team_number=Dashboard.get_team_number(),
            nav_bar=Dashboard.get_nav_bar(),
            active_page=page,
            page_title=Dashboard.get_page_title(page),
            widget_list=Dashboard.get_page_widgets(page))

    @staticmethod
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("pagenotfound.html"), 404

    ### SOCKET.IO EVENTS ###

    @staticmethod
    @sio.on("join")
    def _join(data):
        join_room(data)
        emit("status", f"Joined to {data}")

    ### UTILITIES ###

    @staticmethod
    def get_page_ids():
        return current_app.web_instance.conf_handler.get_page_ids()

    @staticmethod
    def get_team_number():
        return current_app.web_instance.team_number

    @staticmethod
    def get_nav_bar():
        return current_app.web_instance.conf_handler.get_nav_bar()

    @staticmethod
    def get_page_title(page):
        return current_app.web_instance.conf_handler.get_page_title(page)

    @staticmethod
    def get_page_widgets(page):
        return current_app.web_instance.conf_handler.get_page_widgets(page)

    @staticmethod
    def _server_thread(host, port, debug):
        Dashboard.sio.run(Dashboard.app, host=host, port=port, debug=debug) # make sure host is 0.0.0.0 for deployment

def main(**kwargs):
    dashboard = Dashboard(kwargs["conf"], kwargs["vars"], kwargs["addr"], kwargs["port"], team_number=5499, debug=kwargs["debug"])
    def interrupt_handler(sig, frame):
        print("shutting down...")
        dashboard.stop()
        exit(0)
    signal.signal(signal.SIGINT, interrupt_handler)
    dashboard.start()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, help="the path to the configuration file")
    parser.add_argument("-v", "--vars", required=True, help="the path to the variable file")
    parser.add_argument("-a", "--addr", required=True, help="the host address for the dashboard server")
    parser.add_argument("-p", "--port", required=True, help="the port to host the dashboard from (for the FMS, host on port 5800 to 5810")
    parser.add_argument("-d", "--debug", required=False, help="launch the server in debug mode", action="store_true")

    kwargs = vars(parser.parse_args())
    main(**kwargs)