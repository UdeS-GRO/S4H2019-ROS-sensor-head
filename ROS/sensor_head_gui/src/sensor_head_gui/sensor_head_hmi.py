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


class SensorHeadHMIWidget(QtWidgets.QWidget):
    def __init__(self):

        # Start the HMI
        super(SensorHeadHMIWidget, self).__init__()
        ui_file = os.path.join(rospkg.RosPack().get_path(
            'sensor_head_gui'), 'resource', 'sensor_head_hmi.ui')
        loadUi(ui_file, self)


        # TOPIC
        self.xaxis = rospy.Publisher('XAxis', Int32)
        self.yaxis = rospy.Publisher('YAxis', Int32)
        self.zaxis = rospy.Publisher('ZAxis', Int32)


        # SEND INFO
        self.slider_position_axis_x.valueChanged[int].connect(self.xaxis.publish)
        self.slider_position_axis_y.valueChanged[int].connect(self.yaxis.publish)
        self.slider_position_axis_z.valueChanged[int].connect(self.zaxis.publish)


        #self.enable_motor.setCheckable(True)
        #self.enable_motor.toggled[bool].connect(self.ChangeMotorState1)
        #self.enable_motor.setChecked(True)
        #self.enable_motor.setChecked(False)



        # RECEIVE INFO
        #self.motor_sub = rospy.Subscriber(
         #   "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)
