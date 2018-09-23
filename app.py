from flask import Flask
from functools import wraps
import json, time
from datetime import datetime
import random
import pymysql.cursors
app = Flask(__name__)

# Connect to the database
connection = pymysql.connect(host='139.59.51.152',
                             user='root',
                             password='appteamback3nd',
                             db='hillffair',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor()

# DECORATOR
# declares json endpoint given endpoint string
# return simple python option1bject in the function you write
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
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "image_id": 1, "likes": 2}]
def getwall():
    query = cursor.execute("SELECT w.id as id, p.name as name, p.id as rollno, w.id as image_id, (SELECT COUNT(*) FROM likes WHERE post_id=w.id) AS likes FROM wall as w, profile as p WHERE p.id=w.profile_id ORDER BY w.time DESC")
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
        if query:
            return {'status': 'success'}
        else:
            return {'status': 'fail'}

@endpoint('/getleaderboard')
# Sample Response: [{"id": "17mi561", "name": "Daniyaal Khan", "score": 60.0}, {"id": "17mi560", "name": "Check", "score": 10.0}]
def getleaderboard():
    query = cursor.execute("SELECT p.id, p.name, (SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=UNIX_timestamp(timestamp(current_date)+19800)) AS score FROM profile AS p ORDER BY score DESC")
    result = cursor.fetchall()
    return result


@endpoint('/postpoint/<rollno>/<int:points>')
def postpoint(rollno, points):
    query = cursor.execute("INSERT INTO score VALUES(NULL, '"+rollno+"', "+str(points)+", "+str(time.time()+19800)+")")
    if query:
        return {'status': 'success'}
    else:
        return {'status': 'fail'}

@endpoint('/getpoint/<rollno>')
def getpoint(rollno):
    query = cursor.execute("SELECT SUM(amount) AS points FROM score WHERE profile_id = '"+rollno+"' AND time>=UNIX_timestamp(timestamp(current_date)+19800)")
    result = cursor.fetchone()
    return result

@endpoint('/getschedule')
def getschedule():
    query = cursor.execute("SELECT * FROM events")
    result = cursor.fetchall()
    # TODO: Convert the datetime.timedelta format of the time of event in the result JSON array to proper timestamp format
    return query

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

winarray = list(range(1,91))
random.shuffle(winarray)

@endpoint('/gettambolanumber')
def gettambolanumber():
    time = int(datetime(2018, datetime.now().month, datetime.now().day, 22, 0).timestamp())
    current = int(datetime.now().timestamp())
    if(0 <= current - time <= 3600):
        i = ((current - time) // 15) % 90
        return {'number' : winarray[i]}
    else:
        return {'status': 'Unavailable'}

@endpoint('/posttambolaresult')
def posttambolaresult():
    return 'Hello, World!'

@endpoint('/getquiz')
def getquiz():
    # returns 10 random questions from category (day)%num_cat
    NUM_CATEGORIES = 7
    day_of_year = datetime.now().timetuple().tm_yday
    curr_cat = (day_of_year % NUM_CATEGORIES)
    query = cursor.execute("SELECT * FROM quiz WHERE category = %s",curr_cat)
    result = cursor.fetchall()
    # choose random 10 from all these
    random.shuffle(result)
    return {'questions':result[:10]}

@endpoint('/postprofile')
def postprofile():
    return 'Hello, World!'

@endpoint('/getprofile')
def getprofile():
    return 'Hello, World!'

@endpoint('/postwall')
def postwall():
    return 'Hello, World!'

@endpoint('/deletewallpost/<user_id>/<int : image_id>')
def deletewallpost(user_id,image_id):
    query = cursor.execute("DELETE from wall where wall.id='"+image_id+"'")
    if query:
        return {'status': 'success'}
    else:
        return {'status': 'fail'}


if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
