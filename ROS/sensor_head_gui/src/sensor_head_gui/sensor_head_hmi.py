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


class SensorHeadHMIWidget(QtWidgets.QWidget):
    def __init__(self):

        # Start the HMI
        super(SensorHeadHMIWidget, self).__init__()
        ui_file = os.path.join(rospkg.RosPack().get_path(
            'sensor_head_gui'), 'resource', 'sensor_head_hmi.ui')
        loadUi(ui_file, self)


        # TOPIC
        self.pub = rospy.Publisher('test2', Int32)


        # SEND INFO
        self.slider_position_axis_x.valueChanged[int].connect(
            partial(self.change_motor_position, 2))
        self.slider_position_axis_y.valueChanged[int].connect(
            partial(self.change_motor_position, 3))
        self.slider_position_axis_z.valueChanged[int].connect(
            partial(self.change_motor_position, 1))

        self.enable_motor.setCheckable(True)
        self.enable_motor.toggled[bool].connect(self.ChangeMotorState1)
        self.enable_motor.setChecked(True)
        self.enable_motor.setChecked(False)



        # RECEIVE INFO
        self.motor_sub = rospy.Subscriber(
            "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)


    def UpdateMotorsData(self, state):
        """Update the motor dictionnary information with the dynamixel state list

        Arguments:
            state {DynamixelStateList} -- [description]
        """

        self.motors_data = {}
        for motor in state.dynamixel_state:
            self.motors_data[motor.id] = motor.present_position

        self.actual_pos_axis1.setNum(self.motors_data[3])



    def change_motor_position(self, motor_id, desired_position):
        self.pub.publish(desired_position)
        pass


    def ChangeMotorState1(self, desired_state):
        '''
        Will be depreceated
        '''
        self.ControlMotor(3, "Torque_Enable", desired_state)
        # self.ControlMotor(2, "Torque_Enable", desired_state)
        # self.ControlMotor(1, "Torque_Enable", desired_state)
        # if self.enable_motor.isChecked():
        #     self.enable_motor.text = "DISABLE MOTOR"
        # else:
        #     self.enable_motor.text = "ENABLE MOTOR"
        pass

    def ControlMotor(self, id, command, value):
        pass

