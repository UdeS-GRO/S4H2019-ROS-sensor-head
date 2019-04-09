#!/usr/bin/env python
import rospy
from sensor_head_gui.msg import X_Controller
from sensor_msgs.msg import Joy
from Constants import *


class manual_control():
    def callback(self, data):
        """[summary]
        
        Arguments:
            data {[type]} -- [description]
        """
        self.currentData = data
  

    def publishXbox(self, otherunusedparam):
        data = self.currentData
        Xbox = X_Controller()
        vitesse = 32  # degrees # TODO: To be specified in parameter
        deadzone = 0.1

        if(data.axes[2] < 0 or data.axes[5] < 0):
            Xbox.deadman = 1
            if (data.axes[0] > deadzone or data.axes[0] < -deadzone):
                self.z_pos = self.z_pos + vitesse*data.axes[0]
                if (self.z_pos < setHome[0]-setRange[0]/2):
                    self.z_pos = setHome[0]-setRange[0]/2
                elif (self.z_pos > setHome[0]+setRange[0]/2):
                    self.z_pos = setHome[0]+setRange[0]/2
            if (data.axes[3] > deadzone or data.axes[3] < -deadzone):
                self.x_pos = self.x_pos + vitesse*data.axes[3]
                if (self.x_pos < setHome[1]-setRange[1]/2):
                    self.x_pos = setHome[1]-setRange[1]/2
                elif (self.x_pos > setHome[1]+setRange[1]/2):
                    self.x_pos = setHome[1]+setRange[1]/2
            if (data.axes[1] > deadzone or data.axes[1] < -deadzone):
                self.y_pos = self.y_pos + vitesse*data.axes[1]
                if (self.y_pos < setHome[2]-setRange[2]/2):
                    self.y_pos = setHome[2]-setRange[2]/2
                elif (self.y_pos > setHome[2]+setRange[2]/2):
                    self.y_pos = setHome[2]+setRange[2]/2
            if (data.buttons[6] == 1):
                Xbox.home = 1
                self.z_pos = setHome[0]
                self.x_pos = setHome[1]
                self.y_pos = setHome[2]
            else:
                Xbox.home = 0
        else:
            Xbox.deadman = 0

        if (data.buttons[0] == 1):
            Xbox.cellOn = 1

        Xbox.axis.x = round(self.x_pos)
        Xbox.axis.y = round(self.y_pos)
        Xbox.axis.z = round(self.z_pos)

        self.pub_Xbox.publish(Xbox)
        
    
    def __init__(self):
        """[summary]
        """
        self.currentData = Joy()
        self.z_pos = setHome[0]
        self.x_pos = setHome[1]
        self.y_pos = setHome[2]

        # Setting queue_size=2 tells to only keep 2 messages before messages 
        # are being dropped. If it not specified, the publishing is synchronous 
        # by default (will not drop messages). "If you are publishing faster 
        # than rospy can send the messages over the wire, rospy will start 
        # dropping old messages." Here, since we don't want to overload the 
        # motor control with too many messages that are past-due, we can drop 
        # messages by limiting queue_size.
        # See http://wiki.ros.org/rospy/Overview/Publishers%20and%20Subscribers#queue_size:_publish.28.29_behavior_and_queuing
        self.pub_Xbox = rospy.Publisher('Xbox', X_Controller, queue_size=2)
        self.subJoy = rospy.Subscriber("joy", Joy, self.callback, queue_size=2)
        rospy.Timer(rospy.Duration(0.05), self.publishXbox)


if __name__ == '__main__':
    """[summary]
    """

    try:
        rospy.init_node('manualControl', anonymous=True)
        mc = manual_control()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
