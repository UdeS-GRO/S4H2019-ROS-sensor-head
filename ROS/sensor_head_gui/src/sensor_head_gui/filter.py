import rospy
from sensor_msgs.msg import Imu

class FilterFIR():

    def callback(self, data):

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

        for i in self.x_inp:
            X_out = X_out + i/len(self.x_inp)

        for i in self.y_inp:
            Y_out = Y_out + i/len(self.y_inp)           

        for i in self.z_inp:
            Z_out = Z_out + i/len(self.z_inp)

        for i in self.w_inp:
            W_out = W_out + i/len(self.w_inp)

        imu.orientation.x = X_out
        imu.orientation.y = Y_out
        imu.orientation.z = Z_out
        imu.orientation.w = W_out

        #print (X_out)

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
        self.x_inp = [0,0,0,0,0,0,0,0,0,0]
        self.y_inp = [0,0,0,0,0,0,0,0,0,0]
        self.z_inp = [0,0,0,0,0,0,0,0,0,0]
        self.w_inp = [0,0,0,0,0,0,0,0,0,0]

        rospy.Subscriber("/mobile_imu", Imu, self.callback)
        self.mobile_imu_filtered = rospy.Publisher('/mobile_imu_filtered',Imu)

if __name__ == '__main__':
    rospy.init_node("FilterNode")
    fn = FilterFIR()
    rospy.spin()

