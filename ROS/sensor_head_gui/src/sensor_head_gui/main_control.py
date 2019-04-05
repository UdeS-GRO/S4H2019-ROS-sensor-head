import os
import rospkg
import rospy
from python_qt_binding import *
from PyQt5 import *
from PyQt5.QtCore import pyqtSlot
from dynamixel_workbench_msgs.srv import *
from dynamixel_workbench_msgs.msg import *
from functools import partial
from rqt_gui.main import Main
from std_msgs.msg import String
import sys
from std_msgs.msg import Int32

#def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
     
def listener():
     rospy.init_node('listener', anonymous=True)
 
     rospy.Subscriber("Xbox",1)
 
     # spin() simply keeps python from exiting until this node is stopped
     rospy.spin()
  
def __init__(self):
    self.pub = rospy.Publisher('chatter', String, queue_size=10)
    self.rate = rospy.Rate(10)  # 10hz

def refresh(self):
    # while not rospy.is_shutdown():
    hello_str = "hello world %s" % rospy.get_time()
    rospy.loginfo(hello_str)
    self.pub.publish(hello_str)
    self.rate.sleep()
