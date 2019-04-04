import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class ManualControl():

        def __init__(self, publisher):
            self.pub = rospy.Publisher(publisher, Twist, queue_size=10)
            rospy.Subscriber("joy", Joy, self.callback)
            rospy.spin()

        def callback(self, data):
            twist = Twist()
            twist.linear.x = 100*data.axes[0]
            twist.linear.y = 100*data.axes[1]
            twist.linear.z = 100*data.axes[3]
            self.pub.publish(twist)

if __name__ = '__main__'):
		__init__()
