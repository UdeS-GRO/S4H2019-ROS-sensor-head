#!/usr/bin/env python

import os
import rospkg
import rospy
from python_qt_binding import *
from PyQt5 import *
from PyQt5.QtCore import pyqtSlot
from dynamixel_workbench_msgs.srv import *
from dynamixel_workbench_msgs.msg import *
from functools import partial
from std_msgs.msg import Int32
from geometry_msgs.msg import Vector3
from sensor_head_gui.msg import HMI
from sensor_head_gui.msg import ControlSource
from Constants import *
from Source import Source


class SensorHeadHMIWidget(QtWidgets.QWidget):
    def __init__(self):

        # Start the HMI
        super(SensorHeadHMIWidget, self).__init__()
        ui_file = os.path.join(rospkg.RosPack().get_path(
            'sensor_head_gui'), 'resource', 'sensor_head_hmi.ui')
        loadUi(ui_file, self)

        # TOPIC
        # self.xaxis = rospy.Publisher('XAxis', Int32)
        # self.yaxis = rospy.Publisher('YAxis', Int32)
        # self.zaxis = rospy.Publisher('ZAxis', Int32)
        # self.telephone = rospy.Publisher('CB_telephone',)
        # self.hmi = rospy.Publisher('CB_hmi')

        # SEND INFO

        self.slider_position_axis_z.valueChanged[int].connect(
            partial(self.RefreshValue, 1))
        self.slider_position_axis_x.valueChanged[int].connect(
            partial(self.RefreshValue, 2))
        self.slider_position_axis_y.valueChanged[int].connect(
            partial(self.RefreshValue, 3))

        self.src_phone.clicked.connect(
            partial(self.ChangeMode, Source.Mobile.value))
        self.src_HMI.clicked.connect(
            partial(self.ChangeMode, Source.Hmi.value))
        self.src_Xbox.clicked.connect(
            partial(self.ChangeMode, Source.Xbox.value))
        self.Homing.clicked.connect(self.setHome)

        # RECEIVE INFO
        # self.motor_sub = rospy.Subscriber(
        #    "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)

        self.pub_Interface = rospy.Publisher('interface', HMI, queue_size=10)
        self.pubSource = rospy.Publisher(
            '/control_source', ControlSource, queue_size=10)

    def RefreshValue(self, value, axis):
        interface = HMI()
        if (axis == 1):
            interface.axis.z = value
        elif (axis == 2):
            interface.axis.x = value
        elif (axis == 3):
            interface.axis.y = value
        self.pub_Interface.publish(interface)

    def ChangeMode(self, mode, desired_state):
        print "hmidesired_state:", desired_state, "mode:", mode
        if (desired_state == True):
            source = ControlSource()
            source.source = mode
            self.pubSource.publish(source)

        return

    def setHome(self, state):
        self.slider_position_axis_z.value = setHome[0]
        self.slider_position_axis_x.value = setHome[1]
        self.slider_position_axis_y.value = setHome[2]
        return


if __name__ == '__main__':
    """[summary]
    """

    try:
        rospy.init_node('SensorHeadHMIWidget', anonymous=True)
        mc = SensorHeadHMIWidget()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
