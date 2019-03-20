import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class ManualControl(publisher):
	
	def callback(data):
		twist = Twist()
		twist.linear.x = 100*data.axes[0]
		twist.linear.y = 100*data.axes[1]
		twist.linear.z = 100*data.axes[3]
		deadman = 100*data.axes[2]
		pub.publish(twist)
		pub2.publish(deadman)

	def _init_():
		global pub
		global pub2
		pub = rospy.Publisher(publisher),Twist)
		pub2 = rospy.Publisher(publisher),deadman)
		rospy.Subscriber("joy", Joy, callback)
		rospy.spin()

	if __name__ = '__main__'):
		_init_()
