import rospy
from sensor_head_gui.msg import Controller
from sensor_head_gui.msg import Deadman
from sensor_msgs.msg import Joy

class ManualControl():
	
	def callback(self, data):
		controller = Controller()
		deadman = Deadman()
		controller.axis.x = 100*data.axes[0]
		controller.axis.y = 100*data.axes[1]
		controller.axis.z = 100*data.axes[3]
		deadman.switch = 100*data.axes[5]
		self.pub_axis.publish(controller)
		self.pub_deadman.publish(deadman)

	def __init__(self, publisher):

		
		self.pub_axis = rospy.Publisher(publisher, Controller, queue_size=10)
		self.pub_deadman = rospy.Publisher(publisher, Deadman, queue_size=10)
		rospy.Subscriber("joy", Joy, self.callback)
		rospy.spin()


if __name__ == '__main__':
    rospy.init_node('Joy2Turtle')
    mc = ManualControl("MC_pub")
    rospy.spin()
	
		
		
