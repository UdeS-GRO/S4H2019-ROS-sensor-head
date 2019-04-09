#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu
from math import sqrt

class FilterFIR():

    def callback(self, data):
        """[summary]
        
        Arguments:
            data {[type]} -- [description]
        """


        imu = Imu()

        x = data.orientation.x
        y = data.orientation.y
        z = data.orientation.z
        w = data.orientation.w

        self.x_inp.append(x)
        self.y_inp.append(y)
        self.z_inp.append(z)
        self.w_inp.append(w)

        X_out = 0
        Y_out = 0
        Z_out = 0
        W_out = 0
        assert len(self.x_inp)>0
        assert len(self.y_inp)>0
        assert len(self.z_inp)>0
        assert len(self.w_inp)>0
        for i in self.x_inp:
            X_out = X_out + i/len(self.x_inp)

        for i in self.y_inp:
            Y_out = Y_out + i/len(self.y_inp)           

        for i in self.z_inp:
            Z_out = Z_out + i/len(self.z_inp)

        for i in self.w_inp:
            W_out = W_out + i/len(self.w_inp)

        # A quaternion needs to be normalised (be a unit vector) to be valid.
        magnitude = sqrt(X_out**2 + Y_out**2 + Z_out**2 + W_out**2)
        assert magnitude != 0
        imu.orientation.x = X_out/magnitude
        imu.orientation.y = Y_out/magnitude
        imu.orientation.z = Z_out/magnitude
        imu.orientation.w = W_out/magnitude

     
        # print(imu.orientation.x)

        if len(self.x_inp) == 21:
            self.x_inp.pop(0)
        
        if len(self.y_inp) == 21:
            self.y_inp.pop(0)

        if len(self.z_inp) == 21:
            self.z_inp.pop(0)

        if len(self.w_inp) == 21:
            self.w_inp.pop(0)
        #  if (data.axes[0] > deadzone or data.axes[0] < -deadzone):
        #         self.z_pos = self.z_pos + vitesse*data.axes[0]
        #         if (self.z_pos < setHome[0]-setRange[0]/2):
        #             self.z_pos = setHome[0]-setRange[0]/2
        #         elif (self.z_pos > setHome[0]+setRange[0]/2):
        #             self.z_pos = setHome[0]+setRange[0]/2
        #     if (data.axes[3] > deadzone or data.axes[3] < -deadzone):
        #         self.x_pos = self.x_pos + vitesse*data.axes[3]
        #         if (self.x_pos < setHome[1]-setRange[1]/2):
        #             self.x_pos = setHome[1]-setRange[1]/2
        #         elif (self.x_pos > setHome[1]+setRange[1]/2):
        #             self.x_pos = setHome[1]+setRange[1]/2
        #     if (data.axes[1] > deadzone or data.axes[1] < -deadzone):
        #         self.y_pos = self.y_pos + vitesse*data.axes[1]
        #         if (self.y_pos < setHome[2]-setRange[2]/2):
        #             self.y_pos = setHome[2]-setRange[2]/2
        #         elif (self.y_pos > setHome[2]+setRange[2]/2):
        #             self.y_pos = setHome[2]+setRange[2]/2

        self.mobile_imu_filtered.publish(imu)
        return

    def __init__(self):
        """[summary]
        """

        # We fill the filter with "emtpy" or "neutral" quaternions, the identity
        # quaternion, {0,0,0,1}
        self.x_inp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.y_inp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.z_inp = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.w_inp = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        self.v= [0,0,0]


        rospy.Subscriber("/mobile_imu", Imu, self.callback, queue_size=1)
        self.mobile_imu_filtered = rospy.Publisher('/mobile_imu_filtered', Imu, queue_size=1)

if __name__ == '__main__':
    """[summary]
    """

    rospy.init_node("FilterNode")
    fn = FilterFIR()
    rospy.spin()

