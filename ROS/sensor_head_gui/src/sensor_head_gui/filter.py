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

    # x_inp = [0,0,0,0]

    def callback(self, data):

        imu = Imu()

        x = data.orientation.x
        y = data.orientation.y
        z = data.orientation.z
        w = data.orientation.w

        self.x_inp.append(x)
        X = 0
        for i in self.x_inp:
            X = X + i/len(self.x_inp)

        imu.orientation.x = X

        # print (x_inp)
        print (X)

        if len(self.x_inp) == 5:
            self.x_inp.pop(0)

        self.mobile_imu_filtered.publish(imu)
        return

    def __init__(self):
        self.x_inp = [0,0,0,0]
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
