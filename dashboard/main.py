#!/usr/bin/env python3
import threading
from flask import Flask, render_template, current_app, redirect
from flask_socketio import SocketIO, emit, join_room

class Dashboard():
    """This is the main web application class"""
    TEAM_NUMBER = 5499

    app = Flask(__name__)
    sio = SocketIO(app, async_mode="eventlet")
    def __init__(self, team_number):
        with Dashboard.app.app_context():
            current_app.web_instance = self
    
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
    def development():
        return render_template(
            "development.html",
            team_number=Dashboard.TEAM_NUMBER)

    @staticmethod
    @sio.on("join")
    def _join(data):
        join_room(data)
        emit("status", f"Joined to {data}")

    @staticmethod
    def _server_thread():
        Dashboard.sio.run(Dashboard.app, host="127.0.0.1", port=5000) # make sure to change host to 0.0.0.0 for deployment

if __name__ == "__main__":
    thread = threading.Thread(target=Dashboard._server_thread(), name="Dashboard Server", daemon=True)
    thread.start()
    thread.join()