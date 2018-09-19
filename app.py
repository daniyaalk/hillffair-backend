from flask import Flask
app = Flask(__name__)

@app.route('/getwall')
def hello_world():
    return 'Hello, World!'
@app.route('/getlike')
def hello_world():
    return 'Hello, World!'

@app.route('/postlike')
def hello_world():
    return 'Hello, World!'

@app.route('/getleaderboard')
def hello_world():
    return 'Hello, World!'

@app.route('/postpoint')
def hello_world():
    return 'Hello, World!'

@app.route('/getpoint')
def hello_world():
    return 'Hello, World!'

@app.route('/getschedule')
def hello_world():
    return 'Hello, World!'

@app.route('/posteventlike')
def hello_world():
    return 'Hello, World!'

@app.route('/geteventlike')
def hello_world():
    return 'Hello, World!'

@app.route('/getclubs')
def hello_world():
    return 'Hello, World!'

@app.route('/getcoreteam')
def hello_world():
    return 'Hello, World!'

@app.route('/getsponsor')
def hello_world():
    return 'Hello, World!'

@app.route('/gettambolanumber')
def hello_world():
    return 'Hello, World!'

@app.route('/posttambolaresult')
def hello_world():
    return 'Hello, World!'

@app.route('/getquiz')
def hello_world():
    return 'Hello, World!'

@app.route('/postprofile')
def hello_world():
    return 'Hello, World!'

@app.route('/getprofile')
def hello_world():
    return 'Hello, World!'

@app.route('/postwall')
def hello_world():
    return 'Hello, World!'
