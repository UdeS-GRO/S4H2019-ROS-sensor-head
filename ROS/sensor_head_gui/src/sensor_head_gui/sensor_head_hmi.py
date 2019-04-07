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


class SensorHeadHMIWidget(QtWidgets.QWidget):
    def __init__(self):

        # Start the HMI
        super(SensorHeadHMIWidget, self).__init__()
        ui_file = os.path.join(rospkg.RosPack().get_path(
            'sensor_head_gui'), 'resource', 'sensor_head_hmi.ui')
        loadUi(ui_file, self)

        interface = HMI()

        # TOPIC
        self.xaxis = rospy.Publisher('XAxis', Int32)
        self.yaxis = rospy.Publisher('YAxis', Int32)
        self.zaxis = rospy.Publisher('ZAxis', Int32)
        # self.telephone = rospy.Publisher('CB_telephone',)
        # self.hmi = rospy.Publisher('CB_hmi')

       

        # SEND INFO
        
        self.slider_position_axis_x.valueChanged[int].connect(
            partial(self.RefreshValue, 1))
        self.slider_position_axis_y.valueChanged[int].connect(
            partial(self.RefreshValue, 2))
        self.slider_position_axis_z.valueChanged[int].connect(
            partial(self.RefreshValue, 3))


        # self.checkbox_telephone.toggled[bool].connect(self.checkbox_telephone.publish)
        # self.checkbox_hmi.toggled[bool].connect(self.checkbox_hmi.publish)

        # self.enable_motor.setCheckable(True)
        # self.enable_motor.toggled[bool].connect(self.ChangeMotorState1)
        # self.enable_motor.setChecked(True)
        # self.enable_motor.setChecked(False)
        
        
        self.pub_Interface = rospy.Publisher('interface',HMI, queue_size=1)

        #RECEIVE INFO
        # self.motor_sub = rospy.Subscriber(
        #    "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)

    def RefreshValue(self,value,axis):
        if (axis == 1):
            interface.axis.z = value
        elif (axis == 2):
            interface.axis.x = value
        elif (axis == 3):
            interface.axis.z = value
        self.pub_Interface.publish(interface)

if __name__ == '__main__':
    """[summary]
    """

    try:
        rospy.init_node('SensorHeadHMIWidget', anonymous=True)
        mc = SensorHeadHMIWidget()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

