#!/usr/bin/env python3
import threading
import argparse
from flask import Flask, render_template, current_app, redirect
from flask_socketio import SocketIO, emit, join_room

from var_handler import VariableHandler

class Dashboard():
    """This is the main web application class"""
    TEAM_NUMBER = 5499

    app = Flask(__name__)
    sio = SocketIO(app, async_mode="eventlet")
    def __init__(self, team_number):
        with Dashboard.app.app_context():
            current_app.web_instance = self
    
    # redirect to the drive page
    @staticmethod
    @app.route("/")
    def index():
        return redirect(f"/drive")

    @staticmethod
    @app.route("/drive")
    def drive():
        return render_template(
            "drive.html",
            team_number=Dashboard.TEAM_NUMBER)
    
    @staticmethod
    @app.route("/dev")
    def dev():
        return render_template(
            "dev.html",
            team_number=Dashboard.TEAM_NUMBER)

    @staticmethod
    @sio.on("join")
    def _join(data):
        join_room(data)
        emit("status", f"Joined to {data}")

    @staticmethod
    def _server_thread():
        Dashboard.sio.run(Dashboard.app, host="127.0.0.1", port=5800) # make sure to change host to 0.0.0.0 for deployment

def main(**kwargs):
    config_file_path = kwargs["conf"]
    variable_file_path = kwargs["vars"]
    thread = threading.Thread(target=Dashboard._server_thread(), name="Dashboard Server", daemon=True)
    thread.start()
    thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf", required=True, help="the path to the configuration file")
    parser.add_argument("-v", "--vars", required=True, help="the path to the variable file")
    kwargs = vars(parser.parse_args())
    main(**kwargs)