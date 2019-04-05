import os
import rospkg
import rospy
from python_qt_binding import *
from PyQt5 import *
#from PyQt5.QtCore import pyqtSlot
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
 
     rospy.Subscriber("Xbox",10)
 
     # spin() simply keeps python from exiting until this node is stopped
     rospy.spin()

if __name__ == '__main__':
          listener()
