from flask import Flask
from functools import wraps
import json, time
from datetime import datetime
import random
import pymysql.cursors
app = Flask(__name__)


global cursor

# DECORATOR
# declares json endpoint given endpoint string
# return simple python option1bject in the function you write
# example:
# @endpoint("/endpoint_string")
# def function():
#     result = {...}

def endpoint(endpoint):
    def endpoint_decorator(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            # Connect to the database
            global cursor
            connection = pymysql.connect(host='52.41.147.246',
                                         user='quizuser',
                                         password='quizadder',
                                         db='hillffair',
                                         cursorclass=pymysql.cursors.DictCursor)
            cursor = connection.cursor()

            if (connection):
                result = func(*args, **kwargs)
                connection.commit()
                connection.close()
                return json.dumps(result), 200, {'Content-Type': 'text/json'}
            else:
                return "{'error':'Error: no connection to database'}", 500, {'Content-Type': 'text/json'}
        return app.route(endpoint)(decorated_func)
    return endpoint_decorator

@endpoint('/getwall/<int:start>')
# Sample Response: [{"id": 1, "name": "Daniyaal Khan", "rollno": "17mi561", "likes": 2}]
def getwall(start):
    query = cursor.execute("SELECT w.id as id, p.name as name, p.id as rollno, (SELECT COUNT(*) FROM likes WHERE post_id=w.id) AS likes FROM wall as w, profile as p WHERE p.id=w.profile_id ORDER BY w.time DESC LIMIT "+str(start)+", "+str(start+10))
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

@endpoint('/getleaderboard/<int:startfrom>')
# Sample Response: [{"id": "17mi561", "name": "Daniyaal Khan", "score": 60.0}, {"id": "17mi560", "name": "Check", "score": 10.0}]
def getleaderboard(startfrom):
    # print("SELECT p.id, p.name, p.image_url, (SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=UNIX_timestamp(timestamp(current_date)+19800)) AS score FROM profile AS p ORDER BY score DESC")
    query = cursor.execute("SELECT p.id, p.name, p.image_url, (SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=UNIX_timestamp(timestamp(current_date)+19800)) AS score, (SELECT SUM(referal_score) FROM score WHERE profile_id=p.id AND time>=UNIX_timestamp(timestamp(current_date)+19800)) as referal_score FROM profile AS p ORDER BY score DESC LIMIT "+str(startfrom)+", "+str(startfrom+10))
    result = cursor.fetchall()
    return result


@endpoint('/postpoint/<rollno>/<int:points>')
def postpoint(rollno, points):
    query = cursor.execute("INSERT INTO score VALUES(NULL, '"+rollno+"', "+str(points)+", "+str(time.time()+19800)+",0.0)")
    if query:
        return {'status': 'success'}
    else:
        return {'status': 'fail'}

# error aayega
@endpoint('/getpoint/<rollno>')
def getpoint(rollno):
    query = cursor.execute("SELECT SUM(amount) AS points FROM score WHERE profile_id = '"+rollno+"' AND time>=(UNIX_timestamp(timestamp(current_date))+19800)")
    result = cursor.fetchone()
    return result

@endpoint('/getschedule')
def getschedule():
    query = cursor.execute("SELECT name as club_name, event_id,event_name,event_time,club_logo FROM events,clubs WHERE events.club_id=clubs.id")
    result = cursor.fetchall()
    #for x in result:
        #x["event_time"] = x["event_time"].timestamp()
    return result

@endpoint('/posteventlike/<user_id>/<event_id>')
def posteventlike(user_id, event_id):
    userCheck = cursor.execute("SELECT * from profile where id = %s", (user_id))
    if userCheck == 0:
        return {'status': 'No such user'}
    eventCheck = cursor.execute("SELECT * from events where event_id = %s", (event_id))
    if eventCheck == 0:
        return {'status': 'No such event'}
    query = cursor.execute("SELECT * from event_likes where user_id = %s AND event_id = %s", (user_id, event_id))
    if query == 0:
        cursor.execute("INSERT INTO event_likes VALUES (NULL, %s, %s)", (event_id, user_id))
        return {'status': 'success'}
    else:
        return {'status': 'Already Liked'}

@endpoint('/geteventlike/<event_id>')
def geteventlike(event_id):
    query = cursor.execute("SELECT COUNT(*) from event_likes where event_id = %s", event_id)
    result = cursor.fetchone()
    return {'likes': result["COUNT(*)"]}

@endpoint('/getclubs')
def getclubs():
    query = cursor.execute("SELECT * FROM clubs")
    result = cursor.fetchall()
    return result

@endpoint('/getcoreteam')
def getcoreteam():
    query = cursor.execute("SELECT * FROM coreteam")
    result = cursor.fetchall()
    return result

@endpoint('/getsponsor')
def getsponsor():
    query = cursor.execute("SELECT * FROM sponsors")
    result = cursor.fetchall()
    return result

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

@endpoint('/postprofile/<name>/<rollno>/<int:phone_no>/<referal>')
def postprofile(name,rollno,phone_no,referal):
    query = cursor.execute("INSERT into profile value ('"+rollno+"',"+str(phone_no)+",'"+name+"',NULL,'"+referal+"')")
    query1 = cursor.execute("INSERT INTO score VALUES(NULL, '"+rollno+"',0,"+str(time.time()+19800)+",10),(NULL, '"+referal+"',0,"+str(time.time()+19800)+",10)")
    if query and query1:
        return {'status': 'success'}
    else:
        query = cursor.execute("INSERT INTO profile VALUES('"+rollno+"', "+phone_no+", '"+name+"', '', '"+referral+"')")
        query = cursor.execute("INSERT INTO score VALUES(NULL, '"+referral+"', 10.0, "+str(int(time.time()+(60*60*24*30)))+")")


    #query = cursor.execute("INSERT into profile VALUES('"+rollno+"',"+str(phone_no)+",'"+name+"',NULL, NULL)")
    return {'status': 'success'}

@endpoint('/getprofile/<user_id>')
def getprofile(user_id):
    #print("SELECT profile.name as name, profile.id as rollno, profile.image_url as profile_pic, (SELECT SUM(amount) FROM score WHERE profile_id=p.id AND time>=UNIX_timestamp(timestamp(current_date)+19800)) as score FROM profile WHERE profile.id ='"+user_id+"'")
    query = cursor.execute("SELECT profile.name as name, profile.id as rollno, profile.image_url as profile_pic, (SELECT SUM(amount) FROM score WHERE score.profile_id=rollno AND time>=UNIX_timestamp(timestamp(current_date)+19800)) as score FROM profile WHERE profile.id ='"+user_id+"'")
    result = cursor.fetchall()
    # print(result1)
    return result

@endpoint('/deletewallpost/<int:image_id>')
def deletewallpost(image_id):
    query = cursor.execute("DELETE from wall where wall.id='"+str(image_id)+"'")
    if query:
        return {'status': 'success'}
    else:
        return {'status': 'fail'}

@endpoint('/postgamestatus/<user_id>')
def postgamestatus(user_id):
    query = cursor.execute("INSERT into game_status values ('"+user_id+"',0,0)")
    if query:
        return {'status':'success'}
    else:
        return {'status': 'failure'}

@endpoint('/gettambolastatus/<user_id>')
def gettambolastatus(user_id):
    query = cursor.execute("SELECT tambola_status from game_status where user_id='"+user_id+"'")
    result = cursor.fetchone()
    return result

@endpoint('/posttambolastatus/<user_id>/<int:value>')
def posttambolastatus(user_id,value):
    query = cursor.execute("UPDATE game_status set tambola_status = "+str(value)+" where user_id = '"+user_id+"'")
    if query:
        return {'status':'success'}
    else:
        return {'status': 'failure'}

@endpoint('/getquizstatus/<user_id>')
def getquizstatus(user_id):
    query = cursor.execute("SELECT quiz_status from game_status where user_id='"+user_id+"'")
    result = cursor.fetchone()
    return result

@endpoint('/postquizstatus/<user_id>/<int:value>')
def postquizstatus(user_id,value):
    query = cursor.execute("UPDATE game_status set quiz_status = "+str(value)+" where user_id = '"+user_id+"'")
    if query:
        return {'status':'success'}
    else:
        return {'status': 'failure'}

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')
