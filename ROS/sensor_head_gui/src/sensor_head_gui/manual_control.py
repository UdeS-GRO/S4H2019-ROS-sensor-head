import rospy
from geometry_msgs.msg import Twist
from 
from sensor_msgs.msg import Joy

class ManualControl():
	
	def callback(self, data):
		twist = Twist()
		twist.linear.x = 100*data.axes[0]
		twist.linear.y = 100*data.axes[1]
		twist.linear.z = 100*data.axes[3]
		#deadman = 100*data.axes[2]
		self.pub.publish(twist)
		#self.pub2.publish(deadman)

	def __init__(self, publisher):

		
		self.pub = rospy.Publisher(publisher, Twist)
		#self.pub2 = rospy.Publisher(publisher, deadman)
		rospy.Subscriber("joy", Joy, self.callback)
		rospy.spin()


if __name__ == '__main__':
    rospy.init_node('Joy2Turtle')
    mc = ManualControl("MC_pub")
    rospy.spin()
	
		
		
