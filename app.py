from flask import Flask
import pymysql.cursors
app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='139.59.91.181',
                             user='root',
                             password='appteamback3nd',
                             db='Hillffair2k18',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

@app.route('/getwall')
def getwall():
    if(connection):
        query = cursor.execute("SELECT  * FROM Wall")
        result = cursor.fetchone()
        return str(result), 200, {'Content-Type': 'text/json'}
    else:
        return "ERror"

@app.route('/getlike/<int:image_id>')
def getlike(image_id):
        query = cursor.execute("SELECT COUNT(*) AS likes FROM likes WHERE post_id="+str(image_id))
        result = cursor.fetchone()
        return str(result), 200, {'Content-Type': 'text/json'}

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


if __name__ == '__main__':
    app.run(debug = True)
