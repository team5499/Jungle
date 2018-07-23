#!/usr/bin/env python3
import time
import threading
import argparse
import signal
from flask import Flask, render_template, current_app, redirect
from flask_socketio import SocketIO, emit, join_room

from var_handler import VariableHandler

class Dashboard():
    """This is the main web application class"""
    app = Flask(__name__)
    sio = SocketIO(app, async_mode="eventlet")

    def __init__(self, conf_path, var_path, address="127.0.0.1", port=5800, team_number=5499):
        with Dashboard.app.app_context():
            current_app.web_instance = self

        self.team_number = team_number
        self.var_handle = VariableHandler(file_path=var_path)

        self.thread = threading.Thread(target=Dashboard._server_thread, args=[address, port], name="Dashboard Server", daemon=True)

    def stop(self):
        self.thread.join(0)

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
        return render_template(
            f"{page}.html", 
            team_number=current_app.web_instance.team_number)

    ### SOCKET.IO EVENTS ###

    @staticmethod
    @sio.on("join")
    def _join(data):
        join_room(data)
        emit("status", f"Joined to {data}")

    ### UTILITIES ###

    @staticmethod
    def _server_thread(host, port):
        Dashboard.sio.run(Dashboard.app, host=host, port=port) # make sure to change host to 0.0.0.0 for deployment

def main(**kwargs):
    dashboard = Dashboard(kwargs["conf"], kwargs["vars"], kwargs["addr"], kwargs["port"], team_number=5499)
    dashboard.thread.start()
    def interrupt_handler(sig, frame):
        print("shutting down...")
        dashboard.stop()
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.pause()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, help="the path to the configuration file")
    parser.add_argument("-v", "--vars", required=True, help="the path to the variable file")
    parser.add_argument("-a", "--addr", required=True, help="the host address for the dashboard server")
    parser.add_argument("-p", "--port", required=True, help="the port to host the dashboard from (for the FMS, host on port 5800 to 5810")

    kwargs = vars(parser.parse_args())
    main(**kwargs)