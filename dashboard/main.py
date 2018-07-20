from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'index page'

@app.route('/hello/', methods=['GET'])
@app.route('/hello/<name>')
def hello_world(name=None):
   return render_template("hello.html", name=name) 

if __name__ == '__main__':
    app.run()
