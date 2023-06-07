from flask import Flask, render_template, Blueprint
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
import json
import user
video_app = Flask(__name__)
video_app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(video_app)
CORS(video_app)
socketio.init_app(video_app, cors_allowed_origins="*")
users = []

video = Blueprint('video', __name__, url_prefix='/video', template_folder='templates', static_folder='static')

@video.route('/')
def index():
    return render_template('video_index.html')


@video.route("/meeting/<uid>")
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

if __name__ == '__main__':
    socketio.run(video_app)