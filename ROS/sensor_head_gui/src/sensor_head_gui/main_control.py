#!/usr/bin/env python

import os
import sys
from functools import partial
from math import pi

import rospkg
import rospy
from dynamixel_workbench_msgs.msg import *
from dynamixel_workbench_msgs.srv import *
from PyQt5 import *
from python_qt_binding import *
from rqt_gui.main import Main
from sensor_head_gui.msg import X_Controller
from std_msgs.msg import Int32, String

from Constants import *


class main_control():
    def __init__(self):
        """Initialisation function.
        """

        self.motor_range = {}
        self.motor_range['x'] = {}
        self.motor_range['x']['homeMot'] = 400
        self.motor_range['x']['homeAng'] = 0.0
        self.motor_range['x']['minPosMot'] = 200
        self.motor_range['x']['minPosAng'] = -pi/4
        self.motor_range['x']['maxPosMot'] = 600
        self.motor_range['x']['maxPosAng'] = pi/4
        self.motor_range['y'] = {}
        self.motor_range['y']['homeMot'] = 700
        self.motor_range['y']['homeAng'] = 0.0
        self.motor_range['y']['minPosMot'] = 350
        self.motor_range['y']['minPosAng'] = -pi/4
        self.motor_range['y']['maxPosMot'] = 1050
        self.motor_range['y']['maxPosAng'] = pi/4
        self.motor_range['z'] = {}
        self.motor_range['z']['homeMot'] = 1000
        self.motor_range['z']['homeAng'] = 0.0
        self.motor_range['z']['minPosMot'] = 500
        self.motor_range['z']['minPosAng'] = -pi
        self.motor_range['z']['maxPosMot'] = 1500
        self.motor_range['z']['maxPosAng'] = pi
        
        self.x = 0
        self.y = 0
        self.z = 0
        
        try:
            rospy.wait_for_service(
                '/dynamixel_workbench/dynamixel_command', 0.1)
            self.motor_proxy = rospy.ServiceProxy(
                '/dynamixel_workbench/dynamixel_command', DynamixelCommand, persistent=True)  # Enabled persistant connection
            self.subManette = rospy.Subscriber(
                "Xbox", X_Controller, self.change_motor_position)
        except:
            print("WAIT")
            self.timer = rospy.Timer(rospy.Duration(2), self.connect)

        # Set max speed
        # self.commandMotor(1, "Position_P_Gain", 300)
        # self.commandMotor(2, "Position_P_Gain", 300)
        # self.commandMotor(3, "Position_P_Gain", 300)

        # self.commandMotor(1, "Torque_Enable", 1)
        # self.commandMotor(2, "Torque_Enable", 1)
        # self.commandMotor(3, "Torque_Enable", 1)

        # self.commandMotor(1, "Max_Position_Limit", 4000)
        # self.commandMotor(2, "Max_Position_Limit", 1700)
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
            print ("je bouge")
            print self.x, self.y, self.z

        except rospy.ServiceException, e:
            print "Service call failed: %s" % e
            print("Error here")

    def change_motor_position(self, Xbox):
        """[summary]

        Arguments:
            Xbox {[type]} -- [description]
        """

        if(Xbox.deadman == 1):
            if(Xbox.home == True):
                self.home()
            elif(Xbox.axis.z != self.z or Xbox.axis.x != self.x or Xbox.axis.y != self.y):
                self.moveMotor(1, Xbox.axis.z)
                self.z = Xbox.axis.z
                self.moveMotor(2, Xbox.axis.x)
                self.x = Xbox.axis.x
                self.moveMotor(3, Xbox.axis.y)
                self.y = Xbox.axis.y
        # elif(filtre)
        # elif(hmi)

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

    def move_to_xyz(self, x_roll_angle, y_pitch_angle, z_yaw_angle):
        """All angles are in radians

        Arguments:
             x_roll_angle {double} -- [description]
             y_pitch_angle {double} -- [description]
             z_yaw_angle {double} -- [description]
        """
        # Make sure that we at least have a number as an angle
        x_roll_angle = float(x_roll_angle)
        y_pitch_angle = float(y_pitch_angle)
        z_yaw_angle = float(z_yaw_angle)

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
            delta = (motx['maxPosMot']-motx['minPosMot']) / \
                (motx['maxPosAng']-motx['minPosAng'])
            x_cmd = int(round(x_roll_angle*delta + motx['minPosMot'], 0))

        if (y_pitch_angle > moty['maxPosAng']):
            y_cmd = int(moty['maxPosMot'])
        elif (y_pitch_angle < moty['minPosAng']):
            y_cmd = int(moty['minPosMot'])
        else:
            delta = (moty['maxPosMot']-moty['minPosMot']) / \
                (moty['maxPosAng']-moty['minPosAng'])
            y_cmd = int(round(y_pitch_angle*delta + moty['minPosMot'], 0))

        if (z_yaw_angle > motz['maxPosAng']):
            z_cmd = int(motz['maxPosMot'])
        elif (z_yaw_angle < motz['minPosAng']):
            z_cmd = int(motz['minPosMot'])
        else:
            delta = (motz['maxPosMot']-motz['minPosMot']) / \
                (motz['maxPosAng']-motz['minPosAng'])
            z_cmd = int(round(z_yaw_angle*delta + motz['minPosMot'], 0))

        # Making sure that the motor commands are valid. Note that assert
        # statements do not execute if the optimisation is requested (compiled)
        # The assert statements are there to make sure that an impossible
        # contidion isn't true.
        # assert motx['minPosMot'] <= x_cmd <= motx['maxPosMot']
        # assert moty['minPosMot'] <= y_cmd <= moty['maxPosMot']
        # assert motz['minPosMot'] <= z_cmd <= motz['maxPosMot']

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

        self.moveMotor(1, z_cmd)
        self.moveMotor(2, y_cmd)
        self.moveMotor(3, x_cmd)
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
