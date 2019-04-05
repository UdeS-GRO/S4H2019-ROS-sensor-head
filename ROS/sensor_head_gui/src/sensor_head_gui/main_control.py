#!/usr/bin/env python

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
from Constants import *

#def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
class main_control():
     def __init__(self):
          
          try:
               rospy.wait_for_service('/dynamixel_workbench/dynamixel_command', 0.1)
               self.motor_proxy = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
               self.subManette = rospy.Subscriber("Xbox", X_Controller, self.change_motor_position)
          except:
               print("WAIT")
               self.timer = rospy.Timer(rospy.Duration(2), self.connect)
        

        # Set max speed
          # self.commandMotor(1, "Position_P_Gain", 300)
          # self.commandMotor(2, "Position_P_Gain", 300)
          # self.commandMotor(3, "Position_P_Gain", 300)

          # self.commandMotor(1, "Torque_Enable", 1)
          # self.commandMotor(2, "Torque_Enable", 1)
          # self.commandMotor(3, "Torque_Enable", 1)

          # self.commandMotor(1, "Max_Position_Limit", 4000)
          # self.commandMotor(2, "Max_Position_Limit", 1700)
          # self.commandMotor(3, "Max_Position_Limit", 1500)

          # self.motor_sub = rospy.Subscriber(
          #   "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)

     def home(self):
          
          for i in range(0, 3):
               self.commandMotor(i+1, "Goal_Position", setHome[i])
          

     def moveMotor(self, id, pos):
          
          if (pos<setHome[id-1]-setRange[id-1]/2):
               self.commandMotor(id, "Goal_Position", setHome[id-1]-setRange[id-1]/2)
               #print("moveMotor under")
          elif (pos>setHome[id-1]+setRange[id-1]/2):
               self.commandMotor(id, "Goal_Position", setHome[id-1]+setRange[id-1]/2)
               #print("moveMotor over")
          else:
               self.commandMotor(id, "Goal_Position", pos)
               #print(pos)
               #print("moveMotor normal")
          

     def commandMotor(self, id, command, value):
          
          """Sends a request to change the desired position of a motor specified by its ID.

          Arguments:
               motor_id {int} -- ID of the motor. Must match the dynamixel motor's id.
               desired_position {[type]} -- [description]
          """

          rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
          #try:
               
          request = DynamixelCommandRequest()
          request.id = id
          request.addr_name = command
          request.value = value 
          try:        
               self.motor_proxy(request)
               print("je bouge")


          except rospy.ServiceException, e:
               print "Service call failed: %s" % e
               print("Error here")
          
     def change_motor_position(self, Xbox):
       
          if(Xbox.deadman == 1):
               if(Xbox.home == True):
                    self.home()
               elif(Xbox.axis.z != z or Xbox.axis.x != x or Xbox.axis.y != y):
                    self.moveMotor(1, Xbox.axis.z)
                    self.z = Xbox.axis.z
                    self.moveMotor(2, Xbox.axis.x)
                    self.x = Xbox.axis.x
                    self.moveMotor(3, Xbox.axis.y)
                    self.y = Xbox.axis.y
          #elif(filtre)
          #elif(hmi)

     def connect(self, event):
        try:
            rospy.wait_for_service('/dynamixel_workbench/dynamixel_command', 0.1)
            self.motor_proxy = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            self.timer.shutdown()
            print("MOTORS FOUND")
        except:
            self.motors = 0
            print("WAITING FOR DYNAMIXEL MOTORS")


if __name__ == '__main__':
     try:
        rospy.init_node('main', anonymous=True)
        mc = main_control()
        rospy.spin()
     except rospy.ROSInterruptException:
        pass
