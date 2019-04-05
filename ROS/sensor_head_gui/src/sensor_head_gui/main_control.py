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
from sensor_head_gui.msg import X_Controller

#def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
class main_control(self):
     def __init__(self, publisher):

          self.subJoy = rospy.Subscriber("Xbox", X_Controller, self.ControlMotor)
          self.motor_sub = rospy.Subscriber(
            "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)

     def change_motor_positionmotor1(self, data):
        """Sends a request to change the desired position of a motor specified by its ID.

        Arguments:
            motor_id {int} -- ID of the motor. Must match the dynamixel motor's id.
            desired_position {[type]} -- [description]
        """

        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
        try:
          ## motor z
            move_motor = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            request = DynamixelCommandRequest()
            request.id = 1
            request.addr_name = "Goal_Position"
            request.value = data.axis.z
            response = move_motor(request)

          ## motor x
            move_motor = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            request = DynamixelCommandRequest()
            request.id = 2
            request.addr_name = "Goal_Position"
            request.value = data.axis.x
            response = move_motor(request)

          ## motor y
          move_motor = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            request = DynamixelCommandRequest()
            request.id = 3
            request.addr_name = "Goal_Position"
            request.value = data.axis.y
            response = move_motor(request)


        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
            print("Error here")
            

     
if __name__ == '__main__':
          listener()
