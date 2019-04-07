#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Imu

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
        assert norm != 0
        imu.orientation.x = X_out/magnitude
        imu.orientation.y = Y_out/magnitude
        imu.orientation.z = Z_out/magnitude
        imu.orientation.w = W_out/magnitude

        if len(self.x_inp) == 11:
            self.x_inp.pop(0)
        
        if len(self.y_inp) == 11:
            self.y_inp.pop(0)

        if len(self.z_inp) == 11:
            self.z_inp.pop(0)

        if len(self.w_inp) == 11:
            self.w_inp.pop(0)

        self.mobile_imu_filtered.publish(imu)
        return

    def __init__(self):
        """[summary]
        """

        # We fill the filter with "emtpy" or "neutral" quaternions, the identity
        # quaternion, {0,0,0,1}
        self.x_inp = [0,0,0,0,0,0,0,0,0,0]
        self.y_inp = [0,0,0,0,0,0,0,0,0,0]
        self.z_inp = [0,0,0,0,0,0,0,0,0,0]
        self.w_inp = [1,1,1,1,1,1,1,1,1,1]

        rospy.Subscriber("/mobile_imu", Imu, self.callback, queue_size=1)
        self.mobile_imu_filtered = rospy.Publisher('/mobile_imu_filtered', Imu)

if __name__ == '__main__':
    """[summary]
    """

    rospy.init_node("FilterNode")
    fn = FilterFIR()
    rospy.spin()

