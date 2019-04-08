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
from sensor_head_gui.msg import ControleSource
from Constants import *


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

            
        self.src_phone.toggled[bool].connect(partial(self.ChangeMode, 1))
        self.src_HMI.toggled[bool].connect(partial(self.ChangeMode, 2))
        self.src_Xbox.toggle[bool].connect(partial(self.ChangeMode,3))
        self.Homing.clicked.connect(self.setHome)

        # RECEIVE INFO
        # self.motor_sub = rospy.Subscriber(
        #    "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)
        
        self.pub_Interface = rospy.Publisher('interface', HMI, queue_size=10)
        self.pubSource = rospy.Publisher('source',ControleSource, queue_size = 10)

    def RefreshValue(self, value, axis):
        interface = HMI()
        if (axis == 1):
            interface.axis.z = value
        elif (axis == 2):
            interface.axis.x = value
        elif (axis == 3):
            interface.axis.y = value
        self.pub_Interface.publish(interface)

    def ChangeMode(self, desired_state, mode):
        source = ControleSource()

        if(mode == 1):
            source.SOURCE_HMI = desired_state
        elif(mode == 2):
            source.SOURCE_MOBILE = desired_state
        elif(mode == 3):
            source.SOURCE_XBOX = desired_state

        self.pub_Interface.publish(source)

    def setHome(self, state):
        self.slider_position_axis_z.value = setHome[1]
        self.slider_position_axis_x.value = setHome[2]
        self.slider_position_axis_y.value = setHome[3]



if __name__ == '__main__':
    """[summary]
    """

    try:
        rospy.init_node('SensorHeadHMIWidget', anonymous=True)
        mc = SensorHeadHMIWidget()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
