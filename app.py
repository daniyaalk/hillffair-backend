from flask import Flask
from functools import wraps
import json, time
import pymysql.cursors
app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='139.59.91.181',
                             user='root',
                             password='appteamback3nd',
                             db='hillffair',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

# DECORATOR
# declares json endpoint given endpoint string
# return simple python object in the function you write
# example:
# @endpoint("/endpoint_string")
# def function():
#     result = {...}
#     return result
def endpoint(endpoint):
    def endpoint_decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            if (connection):
                result = func(*args, **kwargs)
                connection.commit()
                return json.dumps(result), 200, {'Content-Type': 'text/json'}
            else:
                return "{'error':'Error: no connection to database'}", 500, {'Content-Type': 'text/json'}
        return app.route(endpoint)(decorated_func)
    return endpoint_decorator

@endpoint('/getwall')
def getwall():
    query = cursor.execute("SELECT * FROM wall")
    result = cursor.fetchall()
    return result

@endpoint('/getlike/<int:image_id>')
# Sample Response: {"likes": 2}
def getlike(image_id):
    query = cursor.execute("SELECT COUNT(*) AS likes FROM likes WHERE post_id="+str(image_id))
    result = cursor.fetchone()
    return result


@endpoint('/postlike/<int:image_id>/<user_id>')
def postlike(image_id, user_id):
        query = cursor.execute("INSERT INTO likes VALUES(NULL, '"+user_id+"', "+str(image_id)+")")
        print("INSERT INTO likes VALUES(NULL, '"+user_id+"', "+str(image_id)+")")
        if query:
            return {'status': 'success'}
        else:
            return {'status': 'fail'}

@endpoint('/getleaderboard')
def getleaderboard():
    return 'Hello, World!'

@endpoint('/postpoint')
def postpoint():
    return 'Hello, World!'

@endpoint('/getpoint')
def getpoint():
    return 'Hello, World!'

@endpoint('/getschedule')
def getschedule():
    return 'Hello, World!'

@endpoint('/posteventlike')
def posteventlike():
    return 'Hello, World!'

@endpoint('/geteventlike')
def geteventlike():
    return 'Hello, World!'

@endpoint('/getclubs')
def getclubs():
    return 'Hello, World!'

@endpoint('/getcoreteam')
def getcoreteam():
    return 'Hello, World!'

@endpoint('/getsponsor')
def getsponsor():
    return 'Hello, World!'

@endpoint('/gettambolanumber')
def gettambolanumber():
    return 'Hello, World!'

@endpoint('/posttambolaresult')
def posttambolaresult():
    return 'Hello, World!'

@endpoint('/getquiz')
def getquiz():
    return 'Hello, World!'

@endpoint('/postprofile')
def postprofile():
    return 'Hello, World!'

@endpoint('/getprofile')
def getprofile():
    return 'Hello, World!'

@endpoint('/postwall')
def postwall():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug = True)
