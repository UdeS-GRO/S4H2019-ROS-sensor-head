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


        # TOPIC
        # self.xaxis = rospy.Publisher('XAxis', Int32)
        # self.yaxis = rospy.Publisher('YAxis', Int32)
        # self.zaxis = rospy.Publisher('ZAxis', Int32)
        # self.telephone = rospy.Publisher('CB_telephone',)
        # self.hmi = rospy.Publisher('CB_hmi')

       

        # SEND INFO
        
        self.slider_position_axis_x.valueChanged[int].connect(
            partial(self.RefreshValue, 1))
        self.slider_position_axis_y.valueChanged[int].connect(
            partial(self.RefreshValue, 2))
        self.slider_position_axis_z.valueChanged[int].connect(
            partial(self.RefreshValue, 3))
        self.telephone_bouton.toggled[bool].connect(partial(self.ChangeMode,1))
        self.HMI_bouton.toggled[bool].connect(partial(self.ChangeMode,2))
        self.Homing.toggle[bool].connect(self.setHome)

       


        #RECEIVE INFO
        # self.motor_sub = rospy.Subscriber(
        #    "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)
        self.pub_Interface = rospy.Publisher('interface',HMI, queue_size=10)

    def RefreshValue(self,value,axis):
        interface = HMI()
        if (axis == 1):
            interface.axis.z = value
        elif (axis == 2):
            interface.axis.x = value
        elif (axis == 3):
            interface.axis.z = value
        self.pub_Interface.publish(interface)

    def ChangeMode(self, desired_state, mode):
        interface = HMI()
        if(mode == 1):
            interface.CB_hmi = desired_state
        elif(mode == 2):
            interface.CB_telephone = desired_state
        self.pub_Interface.publish(interface)

    def setHome(self, state):
        interface = HMI()
        interface.home = state
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

