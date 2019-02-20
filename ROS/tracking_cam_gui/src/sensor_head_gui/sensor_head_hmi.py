import os
import rospkg
import rospy
from python_qt_binding import *
from PyQt5 import *
from dynamixel_workbench_msgs.srv import *
from dynamixel_workbench_msgs.msg import *






class SensorHeadHMIWidget(QtWidgets.QWidget):
    def __init__(self):

        # Start the HMI
        super(SensorHeadHMIWidget, self).__init__()
        ui_file = os.path.join(rospkg.RosPack().get_path('tracking_cam_gui'), 'resource', 'sensor_head_hmi.ui')
        loadUi(ui_file, self)


        # SEND INFO
        self.axis_1_position.valueChanged[int].connect(self.change_motor_position)
        self.enable_motor.clicked[bool].connect(self.ChangeMotorState1)


        # RECEIVE INFO
        self.motor_sub = rospy.Subscriber("/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)




    def UpdateMotorsData(self, state):
        '''
        Update the motor dictionnary information with the dynamixel state list
        '''
        self.motors_data = {}
        for motor in state.dynamixel_state:
            self.motors_data[motor.id] = motor.present_position
            self.actual_pos_axis1.setNum(self.motors_data[1])



    def change_motor_position(self, desired_position):
        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
        try:
            move_motor = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            request = DynamixelCommandRequest()
            request.id = 1
            request.addr_name = "Goal_Position"
            request.value = desired_position
            response = move_motor(request)

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e




    def ChangeMotorState1(self, desired_state):
        '''
        Will be depreceated
        '''
        self.ControlMotor(1, "Torque_Enable", desired_state)
        pass




    def ControlMotor(self, id, command, value):
        '''
        TODO: Will become the function used in independant ROS package
        '''
        rospy.wait_for_service('/dynamixel_workbench/dynamixel_command')
        try:
            service_object = rospy.ServiceProxy('/dynamixel_workbench/dynamixel_command', DynamixelCommand)
            request = DynamixelCommandRequest()
            request.id = 1
            request.addr_name = command
            request.value = value
            service_call_response = service_object(request)

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e
