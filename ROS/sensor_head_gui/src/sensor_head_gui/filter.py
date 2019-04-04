import rospy
from sensor_msgs.msg import Imu
# import csv
# import os, rospkg
# rospack = rospkg.RosPack()
# with open(os.path.join(rospack.get_path("_slash_mobile_imu.csv"), "csv", "alarms.csv"), 'rb') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:

# import CSV
# with open('_slash_mobile_imu.csv', 'rb') as f:
#     reader = csv.reader(f)
# for row in reader:
#     print row
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

        # print (x_inp)
        print (X_out)

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
        # global pub 
        # 


if __name__ == '__main__':
    rospy.init_node("FilterNode")
    fn = FilterFIR()
    rospy.spin()

# import rospy
# # from geometry_msgs.msg import Twist
# # from sensor_msgs.msg import Joy

# # from _slash_mobile_imu.csv import x

# class filter_FIR(publisher):
	
#     def init_():


#     def donnee(data):
#         coord = x()
#         coord.x = 



# 	def callback(data):
# 		twist = Twist()
# 		twist.linear.x = 100*data.axes[0]
# 		twist.linear.y = 100*data.axes[1]
# 		twist.linear.z = 100*data.axes[3]
# 		deadman = 100*data.axes[2]
# 		pub.publish(twist)
# 		pub2.publish(deadman)

# 	def _init_():
# 		global pub
# 		global pub2
# 		pub = rospy.Publisher(publisher,Twist)
# 		pub2 = rospy.Publisher(publisher,deadman)
# 		rospy.Subscriber("joy", Joy, callback)
# 		rospy.spin()


# if __name__ == '__main__':
#     rospy.init_node("FilterNode")
#     _init_()
#     rospy.Subscriber("/mobile_imu", Imu, callback)
#     rospy.spin()
