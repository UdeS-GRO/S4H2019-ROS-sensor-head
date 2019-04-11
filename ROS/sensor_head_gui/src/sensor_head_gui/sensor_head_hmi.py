#!/usr/bin/env python

import os
import rospkg
import rospy
from python_qt_binding import *
from PyQt5 import *
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QAbstractSlider
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
    """[summary]
        Node which connect the ROS RQT plugin with the main control.

    """
    def __init__(self):

        # Start the HMI
        super(SensorHeadHMIWidget, self).__init__()
        ui_file = os.path.join(rospkg.RosPack().get_path(
            'sensor_head_gui'), 'resource', 'sensor_head_hmi.ui')
        loadUi(ui_file, self)


        # SEND INFO
        """[summary]
            Connect object of the hmi with variables and fonctions.
        """
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
        """[summary]
            Topic publicher
        """
        self.pub_Interface = rospy.Publisher('interface', HMI, queue_size=10)
        self.pubSource = rospy.Publisher(
            '/control_source', ControlSource, queue_size=10)

    def RefreshValue(self, axis, value):
        """[summary]
            asign value of the slider to the right axis.
        """
        interface = HMI()
        if (axis == 1):
            interface.axis.z = value
            interface.axis.x = self.slider_position_axis_x.value()
            interface.axis.y = self.slider_position_axis_y.value()
        elif (axis == 2):
            interface.axis.x = value
            interface.axis.z = self.slider_position_axis_z.value()
            interface.axis.y = self.slider_position_axis_y.value()
        elif (axis == 3):
            interface.axis.y = value
            interface.axis.z = self.slider_position_axis_z.value()
            interface.axis.x = self.slider_position_axis_x.value()
        self.pub_Interface.publish(interface)

    def ChangeMode(self, mode, desired_state):
        """[summary]
            fonction who asign the wanted mode to the global variable source.
        """
        print ("hmidesired_state:", desired_state, "mode:", mode)
        if (desired_state == True):
            source = ControlSource()
            source.source = mode
            self.pubSource.publish(source)

        return

    def setHome(self, state):
        """[summary]
            fonction who asign home's values to sliders in the hmi.
        """
        
        self.slider_position_axis_z.setValue(setHome[0])
        QtWidgets.qApp.processEvents()
        self.slider_position_axis_x.setValue(setHome[1])
        QtWidgets.qApp.processEvents()
        self.slider_position_axis_y.setValue(setHome[2])
        QtWidgets.qApp.processEvents()
        # self.slider_position_axis_y.triggerAction(QAbstractSlider.SliderMove)
        # self.slider_position_axis_z.triggerAction(QAbstractSlider.SliderMove)
        # self.slider_position_axis_x.triggerAction(QAbstractSlider.SliderMove)
        # QAbstractSlider.SliderMove
        return


if __name__ == '__main__':
    """[summary]
        node initialisation and cration
    """

    try:
        rospy.init_node('SensorHeadHMIWidget', anonymous=True)
        mc = SensorHeadHMIWidget()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
