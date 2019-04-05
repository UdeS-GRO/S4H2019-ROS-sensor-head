#!/usr/bin/env python
import rospy
from sensor_head_gui.msg import X_Controller
from sensor_msgs.msg import Joy


class ManualControl():
    def callback(self, data):
    
        Xbox = X_Controller()
        vitesse = 1  # degrees # TODO: To be specified in parameter
        deadzone = 0.1

        if (data.axes[0]>deadzone || data.axes[0]<-deadzone)
            x_pos = x_pos + vitesse*data.axes[0]
        if (data.axes[1]>deadzone || data.axes[1]<-deadzone)
            y_pos = y_pos + vitesse*data.axes[1]
        if (data.axes[3]>deadzone || data.axes[3]<-deadzone)
            z_pos = z_pos + vitesse*data.axes[3]
        if (data.buttons[6]==1)
            x_pos = 0
            y_pos = 0
            z_pos = 0
        Xbox.axis.x = x_pos
        Xbox.axis.y = y_pos
        Xbox.axis.z = z_pos

        if(data.axes[3] < 0 || data.axes[5] < 0):
            Xbox.deadman = 1
        else:
            Xbox.deadman = 0
            
        self.pub_Xbox.publish(Xbox)

    def __init__(self, publisher):

        self.pub_Xbox = rospy.Publisher(publisher, X_Controller, queue_size=10)
        self.subJoy = rospy.Subscriber("joy", Joy, self.callback)


if __name__ == '__main__':
    rospy.init_node('Joy2Turtle')
    mc = ManualControl("MC_pub")
    rospy.spin()
