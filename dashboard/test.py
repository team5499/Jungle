from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
app = Flask(__name__)

@app.route("/")
def index():
    return "index page"

@app.route("/test/hello", methods=["GET"])
@app.route("/test/hello/<name>", methods=["GET"])
def hello_world(name=None):
   return render_template("test.html", name=name)



if __name__ == "__main__":
    app.run()
