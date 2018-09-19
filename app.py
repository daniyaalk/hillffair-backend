from flask import Flask
app = Flask(__name__)

@app.route('/getwall')
def getwall():
    return 'Hello, World!'
@app.route('/getlike')
def getlike():
    return 'Hello, World!'

@app.route('/postlike')
def postlike():
    return 'Hello, World!'

@app.route('/getleaderboard')
def getleaderboard():
    return 'Hello, World!'

@app.route('/postpoint')
def postpoint():
    return 'Hello, World!'

@app.route('/getpoint')
def getpoint():
    return 'Hello, World!'

@app.route('/getschedule')
def getschedule():
    return 'Hello, World!'

@app.route('/posteventlike')
def posteventlike():
    return 'Hello, World!'

@app.route('/geteventlike')
def geteventlike():
    return 'Hello, World!'

@app.route('/getclubs')
def getclubs():
    return 'Hello, World!'

@app.route('/getcoreteam')
def getcoreteam():
    return 'Hello, World!'

@app.route('/getsponsor')
def getsponsor():
    return 'Hello, World!'

@app.route('/gettambolanumber')
def gettambolanumber():
    return 'Hello, World!'

@app.route('/posttambolaresult')
def posttambolaresult():
    return 'Hello, World!'

@app.route('/getquiz')
def getquiz():
    return 'Hello, World!'

@app.route('/postprofile')
def postprofile():
    return 'Hello, World!'

@app.route('/getprofile')
def getprofile():
    return 'Hello, World!'

@app.route('/postwall')
def postwall():
    return 'Hello, World!'
