#!/usr/bin/env python

import os
import sys
from functools import partial
from math import pi, atan2, asin

import rospkg
import rospy
from dynamixel_workbench_msgs.msg import *
from dynamixel_workbench_msgs.srv import *
from PyQt5 import *
from python_qt_binding import *
from rqt_gui.main import Main
from sensor_head_gui.msg import X_Controller
from sensor_head_gui.msg import HMI
from sensor_head_gui.msg import ControlSource
from std_msgs.msg import Int32, String
from geometry_msgs.msg import Vector3
from sensor_msgs.msg import Imu
from Constants import *
from Source import Source


class main_control():
    def __init__(self):
        """Initialisation function.
        """

        self.motor_range = {}
        self.motor_range['x'] = {}
        self.motor_range['x']['homeMot'] = 683
        self.motor_range['x']['homeAng'] = 0.0
        self.motor_range['x']['minPosMot'] = 0
        self.motor_range['x']['minPosAng'] = -(pi/3) * 2
        self.motor_range['x']['maxPosMot'] = 1535
        self.motor_range['x']['maxPosAng'] = (pi/3)*2
        self.motor_range['y'] = {}
        self.motor_range['y']['homeMot'] = 768
        self.motor_range['y']['homeAng'] = 0.0
        self.motor_range['y']['minPosMot'] = 0
        self.motor_range['y']['minPosAng'] = -(3*pi/8)*2
        self.motor_range['y']['maxPosMot'] = 1535
        self.motor_range['y']['maxPosAng'] = (3*pi/8)*2
        self.motor_range['z'] = {}
        self.motor_range['z']['homeMot'] = 2048
        self.motor_range['z']['homeAng'] = 0.0
        self.motor_range['z']['minPosMot'] = 0
        self.motor_range['z']['minPosAng'] = -pi
        self.motor_range['z']['maxPosMot'] = 4095
        self.motor_range['z']['maxPosAng'] = pi

        self.x = 0
        self.y = 0
        self.z = 0

        self.gyropos = [0, 0, 0]

        self.cellOn = False
        self.timer = 0
        self.currentSource = Source.Xbox  # Xbox

        rospy.on_shutdown(self.shutdown_hook)
        try:
            rospy.wait_for_service(
                '/dynamixel_workbench/dynamixel_command', 2)

            self.motor_proxy = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand,
                persistent=True)  # Enabled persistant connection

            self.subManette = rospy.Subscriber(
                "Xbox", X_Controller, self.callbackXbox, queue_size=2)

            # self.subMobileImuFiltered = rospy.Subscriber(
            #     "/mobile_imu_filtered", Imu, self.callbackMobile, queue_size=1)
            # self.subMobileImuFiltered = rospy.Subscriber(
            #     "/mobile_imu", Imu, self.callbackMobile, queue_size=1)

            self.subMobileImuFiltered = rospy.Subscriber(
                "/mobile_imu", Vector3, self.callbackMobile2, queue_size=1)
            self.subHMI = rospy.Subscriber(
                "/interface", HMI, self.callbackHMI, queue_size=1)

            self.subControlSource = rospy.Subscriber(
                "/control_source", ControlSource, self.callbackCtrlSrc, queue_size=10)

        except:
            print("WAIT")
            self.timer = rospy.Timer(rospy.Duration(2), self.connect)

        # Set max speed
        # self.commandMotor(1, "Position_P_Gain", 640)
        # self.commandMotor(2, "Position_P_Gain", 800)
        # self.commandMotor(3, "Position_P_Gain", 640)

        # self.commandMotor(1, "Torque_Enable", 1)
        # self.commandMotor(2, "Torque_Enable", 1)
        # self.commandMotor(3, "Torque_Enable", 1)filt

        # self.commandMotor(1, "Max_Position_Limitfilt
        # self.commandMotor(2, "Max_Position_Limitfilt
        # self.commandMotor(3, "Max_Position_Limit", 1500)

        # self.motor_sub = rospy.Subscriber(
        #   "/dynamixel_workbench/dynamixel_state", DynamixelStateList, self.UpdateMotorsData)

        # Note that "assert" statements do not execute if the optimisation is
        # requested (compiled). The assert statements are there to make sure
        # that an impossible contidion isn't true. Thats why we explicitly
        # check for invalid configuration given that would produce wrong
        # computed commands
        if not self.motor_range['x']['minPosMot'] <= self.motor_range['x']['homeMot'] <= self.motor_range['x']['maxPosMot']:
            raise AssertionError
        if not self.motor_range['y']['minPosMot'] <= self.motor_range['y']['homeMot'] <= self.motor_range['y']['maxPosMot']:
            raise AssertionError
        if not self.motor_range['z']['minPosMot'] <= self.motor_range['z']['homeMot'] <= self.motor_range['z']['maxPosMot']:
            raise AssertionError
        if not self.motor_range['x']['minPosAng'] <= self.motor_range['x']['homeAng'] <= self.motor_range['x']['maxPosAng']:
            raise AssertionError
        if not self.motor_range['y']['minPosAng'] <= self.motor_range['y']['homeAng'] <= self.motor_range['y']['maxPosAng']:
            raise AssertionError
        if not self.motor_range['z']['minPosAng'] <= self.motor_range['z']['homeAng'] <= self.motor_range['z']['maxPosAng']:
            raise AssertionError

    def shutdown_hook(self):
        self.timer.shutdown()

    def connect(self, event):
        """[summary]

        Arguments:
            event {[type]} -- [description]
        """

        try:
            rospy.wait_for_service(
                '/dynamixel_workbench/dynamixel_command', 0.1)
            self.motor_proxy = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand, persistent=True)
            self.timer.shutdown()
            print("MOTORS FOUND")
        except:
            self.motors = 0
            print("WAITING FOR DYNAMIXEL MOTORS")

    def home(self):
        """[summary]
        """
        for i in range(0, 3):
            self.commandMotor(i+1, "Goal_Position", setHome[i])

    def moveMotor(self, id, pos):
        """[summary]

        Arguments:
            id {[type]} -- [description]
            pos {[type]} -- [description]
        """

        if (pos < setHome[id-1]-setRange[id-1]/2):
            self.commandMotor(id, "Goal_Position",
                              setHome[id-1]-setRange[id-1]/2)
            # print("moveMotor under")
        elif (pos > setHome[id-1]+setRange[id-1]/2):
            self.commandMotor(id, "Goal_Position",
                              setHome[id-1]+setRange[id-1]/2)
            # print("moveMotor over")
        else:
            self.commandMotor(id, "Goal_Position", pos)
            # print(pos)
            # print("moveMotor normal")

    def commandMotor(self, id, command, value):
        """Sends a command to a motor specified by its ID.

        Arguments:
            id {int} -- ID of the motor. Must match the dynamixel motor's id.
            command {[type]} -- [description]
            value {[type]} -- [description]
        """

        # rospy.wait_for_service('/dynamixel_workbench/dynamixel_command') # Only at initialisation
        # try:

        request = DynamixelCommandRequest()
        request.id = id
        request.addr_name = command
        request.value = value
        try:
            self.motor_proxy(request)
            print self.x, self.y, self.z

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
            print("Error here")

    def callbackXbox(self, Xbox):
        """[summary]

        Arguments:
            Xbox {[type]} -- [description]
        """
        # Only process control if the current source is given to Xbox
        if (self.currentSource == Source.Xbox):

            # Send Xbox commands only when the deadman switch is held on.
            if(Xbox.deadman == 1):
                if(Xbox.home == True):
                    self.home()
                else:
                    if(Xbox.axis.z != self.z):
                        self.moveMotor(1, Xbox.axis.z)
                        self.z = Xbox.axis.z
                    if(Xbox.axis.x != self.x):
                        self.moveMotor(2, Xbox.axis.x)
                        self.x = Xbox.axis.x
                    if(Xbox.axis.y != self.y):
                        self.moveMotor(3, Xbox.axis.y)
                        self.y = Xbox.axis.y

        self.cellOn = Xbox.cellOn

    def callbackHMI(self, data):
        """[summary]

        Arguments:
            data {[type]} -- [description]
        """
        print "hmimsg called"
        if (self.currentSource == Source.Hmi):
            print "hmi msg:", data
            if(data.axis.z != self.z):
                self.moveMotor(1, data.axis.z)
                self.z = data.axis.z
            if(data.axis.x != self.x):
                self.moveMotor(2, data.axis.x)
                self.x = data.axis.x
            if(data.axis.y != self.y):
                self.moveMotor(3, data.axis.y)
                self.y = data.axis.y

        return

    def callbackCtrlSrc(self, data):
        """Processes the current source input set by the HMI.

        Arguments:
            data {ControlSource} -- Contains the source number that should take the control 
        """

        print "source act:", self.currentSource, "new:", data
        if (data.source == data.SOURCE_HMI):
            self.currentSource = Source.Hmi

        elif (data.source == data.SOURCE_XBOX):
            self.currentSource = Source.Xbox

        elif (data.source == data.SOURCE_MOBILE):
            self.currentSource = Source.Mobile

        else:
            self.currentSource = Source.Xbox

        return

    def callbackMobile(self, data):
        """[summary]

        Arguments:
            data {[type]} -- [description]
        """

        if (self.currentSource == Source.Mobile):
            # print "oui"

            euler_or = self.quat_to_euler(data.orientation)
            self.move_to_xyz(euler_or['roll'],
                             euler_or['pitch'], euler_or['yaw'])
        return

    def quat_to_euler(self, orientation):
        """[summary]

        Arguments:
            orientation {[type]} -- [description]

        Returns:
            [type] -- [description]
        """

        x = orientation.x
        y = orientation.y
        z = orientation.z
        w = orientation.w

        # roll = atan2(2*(x*y+z*w), 1-(2*(y**2+z**2)))
        # pitch = asin(2*(x*y-z*w))
        # yaw = atan2(2*(x*w+y*z), 1-(2*(z**2+w**2)))

        test = x * y + z * w

        if (test > 0.499):
            yaw = 2 * atan2(x, w)
            pitch = pi / 2
            roll = 0

            euler1 = [pitch, roll, yaw]
            return euler1

        if (test < -0.499):
            yaw = -2 * atan2(x, w)
            pitch = -pi / 2
            roll = 0
            euler2 = [pitch, roll, yaw]
            return euler2

        sqx = x * x
        sqy = y * y
        sqz = z * z
        yaw = atan2(2 * y * w - 2 * x * z, 1 - 2 * sqy - 2 * sqz)
        pitch = asin(2 * test)
        roll = atan2(2 * x * w - 2 * y * z, 1 - 2 * sqx - 2 * sqz)

        # euler = [pitch, roll, yaw]
        angles = {'roll': roll, 'pitch': pitch, 'yaw': yaw}

        return angles

    def move_to_xyz(self, x_roll_angle, y_pitch_angle, z_yaw_angle):
        """All angles are in radians

        Arguments:
             x_roll_angle {double} -- [description]
             y_pitch_angle {double} -- [description]
             z_yaw_angle {double} -- [description]
        """
        # print "angle in", x_roll_angle, y_pitch_angle, z_yaw_angle
        # Make sure that we at least have a number as an angle
        x_roll_angle = float(x_roll_angle)
        y_pitch_angle = float(y_pitch_angle)
        z_yaw_angle = float(z_yaw_angle)
        # print "angle float", x_roll_angle, y_pitch_angle, z_yaw_angle

        # Creating a local copy to minimise calls to class member
        motx = self.motor_range['x']
        moty = self.motor_range['y']
        motz = self.motor_range['z']

        # Clipping invalid results, or interpolating and creating a motor
        # command. (With angle * delta_motorPos/delta_angle)
        if (x_roll_angle > motx['maxPosAng']):
            x_cmd = int(motx['maxPosMot'])
        elif (x_roll_angle < motx['minPosAng']):
            x_cmd = int(motx['minPosMot'])
        else:
            angle = x_roll_angle - motx['minPosAng']
            delta = (motx['maxPosMot']-motx['minPosMot']) / \
                (motx['maxPosAng']-motx['minPosAng'])
            x_cmd = int(round(angle*delta + motx['minPosMot'], 0))

        if (y_pitch_angle > moty['maxPosAng']):
            y_cmd = int(moty['maxPosMot'])
        elif (y_pitch_angle < moty['minPosAng']):
            y_cmd = int(moty['minPosMot'])
        else:
            angle = y_pitch_angle - moty['minPosAng']
            delta = (moty['maxPosMot']-moty['minPosMot']) / \
                (moty['maxPosAng']-moty['minPosAng'])
            y_cmd = int(round(angle*delta + moty['minPosMot'], 0))

        if (z_yaw_angle > motz['maxPosAng']):
            z_cmd = int(motz['maxPosMot'])
        elif (z_yaw_angle < motz['minPosAng']):
            z_cmd = int(motz['minPosMot'])
        else:
            angle = z_yaw_angle - motz['minPosAng']
            delta = (motz['maxPosMot']-motz['minPosMot']) / \
                (motz['maxPosAng']-motz['minPosAng'])
            z_cmd = int(round(angle*delta + motz['minPosMot'], 0))
            # print delta, z_cmd

        # Making sure that the motor commands are valid. Note that assert
        # statements do not execute if the optimisation is requested (compiled)
        # The assert statements are there to make sure that an impossible
        # contidion isn't true.
        # assert motx['minPosMot'] <= x_cmd <= motx['maxPosMot']
        # assert moty['minPosMot'] <= y_cmd <= moty['maxPosMot']
        # assert motz['minPosMot'] <= z_cmd <= motz['maxPosMot']

        print "x", x_roll_angle, x_cmd  # , motx
        print "y", y_pitch_angle, y_cmd  # , moty
        print "z", z_yaw_angle, z_cmd  # , motz

        # On second thought, to make the system catch internal error, let's make
        # sure the tests are checked even when optimisation is on.
        if not motx['minPosMot'] <= x_cmd <= motx['maxPosMot']:
            raise AssertionError, "Motor command about to be sent is out of bounds"
        if not moty['minPosMot'] <= y_cmd <= moty['maxPosMot']:
            raise AssertionError, "Motor command about to be sent is out of bounds"
        if not motz['minPosMot'] <= z_cmd <= motz['maxPosMot']:
            raise AssertionError, "Motor command about to be sent is out of bounds"

        # print "x", x_roll_angle, x_cmd
        # print "y", y_pitch_angle, y_cmd
        # print "z", z_yaw_angle, z_cmd

        # self.moveMotor(1, z_cmd)
        self.moveMotor(2, y_cmd)
        self.moveMotor(3, x_cmd)
        # pass

    def callbackMobile2(self, vector3data):

        if (self.currentSource == Source.Mobile):
            factor = 1
            self.gyropos[0] += factor*vector3data.x
            self.gyropos[1] += factor*vector3data.y
            self.gyropos[2] += factor*vector3data.z

            motx = self.motor_range['x']
            moty = self.motor_range['y']
            motz = self.motor_range['z']

            if (self.gyropos[2] < setHome[0]-setRange[0]/2):
                self.gyropos[2] = setHome[0]-setRange[0]/2
            elif (self.gyropos[2] < setHome[0]+setRange[0]/2):
                self.gyropos[2] = setHome[0]+setRange[0]/2

            if (self.gyropos[0] < setHome[1]-setRange[1]/2):
                self.gyropos[0] = setHome[1]-setRange[1]/2
            elif (self.gyropos[0] < setHome[1]+setRange[1]/2):
                self.gyropos[0] = setHome[1]+setRange[1]/2

            if (self.gyropos[1] < setHome[2]-setRange[2]/2):
                self.gyropos[1] = setHome[2]-setRange[2]/2
            elif (self.gyropos[1] < setHome[2]+setRange[2]/2):
                self.gyropos[1] = setHome[2]+setRange[2]/2

            print self.gyropos
            # self.moveMotor(1, self.gyropos[2])
            # self.moveMotor(2, self.gyropos[0])
            self.moveMotor(3, self.gyropos[1])

        pass


if __name__ == '__main__':
    """[summary]
    """

    try:
        rospy.init_node('main', anonymous=True)
        mc = main_control()
        rospy.spin()
        # Tests:
        # mr = motor_range()
        # print mr.motor_range['x']
        # print mr.motor_range['y']
        # print mr.motor_range['z']

        # mr.move_to_xyz(-1.2234, 0.1, '0')
        # mr.move_to_xyz(56, 0.24, 2345.2)
        # # mr.move_to_xyz("324",{'x':23.4}, (-0.62))
        # # mr.move_to_xyz("", 'a', [0.4])
    except rospy.ROSInterruptException:
        pass
