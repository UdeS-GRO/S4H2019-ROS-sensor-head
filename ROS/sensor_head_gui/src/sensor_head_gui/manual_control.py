import rospy
from sensor_head_gui.msg import X_Controller
from sensor_msgs.msg import Joy

class ManualControl():
	
	def callback(self, data):
		Xbox = X_Controller()
		vitesse = 1 #degrés
		
		x_pos = x_pos + vitesse*data.axes[0]/32767
		y_pos = y_pos + vitesse*data.axes[1]/32767
		z_pos = z_pos + vitesse*data.axes[3]/32767
		Xbox.axis.x = x_pos
		Xbox.axis.y = y_pos
		Xbox.axis.z = z_pos
		
		if(data.axes[5]>0)
		    Xbox.deadman = 1
		else
		    Xbox.deadman = 0
		self.pub_Xbox.publish(Xbox)

	def __init__(self, publisher):

		self.pubController = rospy.Publisher(publisher, X_Controller, queue_size=10)
		self.subJoy = rospy.Subscriber("joy", Joy, self.callback)


if __name__ == '__main__':
    rospy.init_node('Joy2Turtle')
    mc = ManualControl("MC_pub")
    rospy.spin()
	
		
		
