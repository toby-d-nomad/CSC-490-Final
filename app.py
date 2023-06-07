from __future__ import absolute_import
from datetime import timedelta
import random
from flask_socketio import SocketIO, send, emit
import string
from flask import Flask, Blueprint, render_template, redirect, url_for, session, json
import os
from flask_mail import Mail, Message
from flask_cors import CORS, cross_origin
from flask_session import Session
from admin.routes import admin
from index.routes import index
from instructor.routes import instructor
from video_meet.main import video
from student.routes import student
import user
users=[]



app = Flask(__name__)
socketio=SocketIO(app, logger=True, engineio_logger=True)
app.secret_key = 'johnnywhitecdfvfdcvdfbvdfbdfgvfdgvdfgvdf433'
app.config['MAIL_SERVER']='smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'jonikwiria@outlook.com'
app.config['MAIL_PASSWORD'] = 'dfsedfse'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)
sender = 'jonikwiria@outlook.com'
SESSION_TYPE='filesystem'
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
UPLOAD_FOLDER = 'static/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SESSION_TYPE'] = 'filesystem'
ALLOWED_EXTENSIONS = set(['pdf', 'xlsx'])

question_extension=set(['txt'])
  
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_question_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in question_extension

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config.from_object(__name__)

sess = Session()
sess.init_app(app)

CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/meeting/<uid>")
def meeting(uid):
    return render_template("meeting.html")


@socketio.on('newUser')
def newUser(msg):
    print('New user: '+msg)
    data = json.loads(msg)
    print(data["username"])
    newuser = user.User(data["username"], data["meetingID"], data["userID"])
    users.append(newuser)
    emit('newUser',msg, broadcast=True)


@socketio.on('checkUser')
def checkUser(msg):
    data = json.loads(msg)
    existing = False
    print(users)
    for user in users:
        print(user.username)
        if(data["username"] == user.username):
            if(data["meetingID"] == user.meetingID):
                existing = True
    if (existing):
        send('userExists', broadcast=False)
    else:
        send('userOK', broadcast=False)


@socketio.on('userDisconnected')
def onDisconnect(msg):
    i = 0
    posArray = 0
    data = json.loads(msg)
    for user in users:
        if(data["username"] == user.username):
            if(data["meetingID"] == user.meetingID):
                posArray = i
        i = i + 1
    users.pop(posArray)
    print("user "+ data["username"]+ " from meeting "+data["meetingID"]+ " disconnected")
    emit('userDisconnected',msg, broadcast=True)
    
@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)





def send_mail(Msg, MsgBody, sendTo, otp):
    msg1 = Message(Msg, sender = sender, recipients = [sendTo])
    msg1.body = str(MsgBody) + ' ' +  str(otp) + '.'
    mail.send(msg1)

def random_string(letter_count, digit_count):  
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))  
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))  
  
    sam_list = list(str1) # it converts the string to list.  
    random.shuffle(sam_list) # It uses a random.shuffle() function to shuffle the string.  
    final_string = ''.join(sam_list)  
    return final_string 

@app.errorhandler(405)
def not_found(e):
    return redirect(url_for('index.main'))

@app.errorhandler(404)
def not_found(e):
  return redirect(url_for('index.main'))

@app.before_first_request  # runs before FIRST request (only once)
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


app.register_blueprint(admin)
app.register_blueprint(index)
app.register_blueprint(instructor)
app.register_blueprint(student)
app.register_blueprint(video)
app

if __name__ == '__main__':
   socketio.run(app, debug=True)