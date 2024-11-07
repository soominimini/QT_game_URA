import numpy as np
from flask import Flask, render_template, redirect, url_for, session, request
from flask_socketio import SocketIO, emit, join_room
import random
import time
import threading
import rospy
from std_msgs.msg import String
from anytree import Node, RenderTree
from qt_robot_interface.srv import *
from qt_gesture_controller.srv import *
from std_msgs.msg import Float64MultiArray


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Robot movements based on dice face
def move_robot_arm():
    # Define arm movement positions (for example, for both arms)
    right_arm = Float64MultiArray(data=[1.5, -0.5, 0.5, -1.5])
    left_arm = Float64MultiArray(data=[-1.5, 0.5, -0.5, 1.5])

    # Publish arm movements
    right_pub.publish(right_arm)
    left_pub.publish(left_arm)

@socketio.on('dice_face_in')
def dice_face_in(activity):
    print("dice_face_in: ", activity)

    if activity == 0:
        rospy.sleep(1)
        talktext_pub.publish("Click again")
    else:
        rospy.sleep(1)
        talktext_pub.publish("It is " + str(activity))
        rospy.sleep(2)
        #talktext_pub.publish("Let's do " + str(activity))

        # Robot action based on activity (based on the dice face)
        if str(activity) == "Jumping Jacks":
            talktext_pub.publish("Let's do 10 jummping jacks!")
            gesturePlay_pub.publish("jumping_jacks")
        elif str(activity) == "Count to 5":
            talktext_pub.publish("Let's count to 5!")
            talktext_pub.publish("1, 2, 3, 4, 5")
            gesturePlay_pub.publish("QT/breathing_exercise")
        elif str(activity) == "Sing a Song":
            talktext_pub.publish("Let's sing a song!")
            #gesturePlay_pub.publish("QT/clap")
            #gesturePlay_pub.publish("my_gesture")
        elif str(activity) == "Wiggle":
            talktext_pub.publish("Let's wiggle our body!")
            talktext_pub.publish("1, 2, 3, 4, 5, 6, 7, 8, 9, 10")
            gesturePlay_pub.publish("wiggle_body")
        elif str(activity) == "Bear Hug":
            talktext_pub.publish("Let's give a hug!")
            talktext_pub.publish("1, 2, 3, 4, 5")
            gesturePlay_pub.publish("hug")
        elif str(activity) == "High Five":
            talktext_pub.publish("Give me a high five!")
            gesturePlay_pub.publish("high_five")




@app.route('/')
def start_page_dice_emotion_young():
    talktext_pub.publish("Let's roll the dice")
    return render_template('dice.html')

if __name__ == '__main__':
    threading.Thread(target=lambda: rospy.init_node('app',
                                                    disable_signals=True)).start()  # it helps to start the rospy and ends terminal

    # Publishers for robot actions
    speechSay_pub = rospy.Publisher('/qt_robot/speech/say', String, queue_size=10)
    talktext_pub = rospy.Publisher('/qt_robot/behavior/talkText', String, queue_size=10)
    gesturePlay_pub = rospy.Publisher('/qt_robot/gesture/play', String, queue_size=10)
    emotionShow_pub = rospy.Publisher('/qt_robot/emotion/show', String, queue_size=10)
    audioPlay_pub = rospy.Publisher('/qt_robot/audio/play', String, queue_size=10)

    # Arm movement publishers
    right_pub = rospy.Publisher('/qt_robot/right_arm_position/command', Float64MultiArray, queue_size=1)
    left_pub = rospy.Publisher('/qt_robot/left_arm_position/command', Float64MultiArray, queue_size=1)

    # Service proxies for robot actions
    gesturePlay_servc = rospy.ServiceProxy('/qt_robot/gesture/play', gesture_play)
    rospy.wait_for_service('/qt_robot/gesture/play')

    socketio.run(app, host='0.0.0.0', debug=True)  # connect to 192.168.100.2:5000 in web
