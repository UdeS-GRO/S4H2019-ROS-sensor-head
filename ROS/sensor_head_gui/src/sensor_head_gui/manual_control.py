#!/usr/bin/env python
import rospy
from sensor_head_gui.msg import X_Controller
from sensor_msgs.msg import Joy

def talker():

    Xbox = X_Controller()
    vitesse = 1  # degrees # TODO: To be specified in parameter
    deadzone = 0.1
    x_pos = 0
    y_pos = 0
    z_pos = 0
    
    pub_Xbox = rospy.Publisher('Xbox', X_Controller, queue_size=10)
    subJoy = rospy.Subscriber("joy", Joy, talker)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        if (data.axes[0]>deadzone || data.axes[0]<-deadzone):
            x_pos = x_pos + vitesse*data.axes[0]
        if (data.axes[1]>deadzone || data.axes[1]<-deadzone):
            y_pos = y_pos + vitesse*data.axes[1]
        if (data.axes[3]>deadzone || data.axes[3]<-deadzone):
            z_pos = z_pos + vitesse*data.axes[3]
        if (data.buttons[6]==1):
            x_pos = 0
            y_pos = 0
            z_pos = 0
        Xbox.axis.x = x_pos
        Xbox.axis.y = y_pos
        Xbox.axis.z = z_pos

        if(data.axes[3] < 0 || data.axes[5] < 0):
            Xbox.deadman = 1
        else:
             Xbox.deadman = 0
        
        #rospy.loginfo(Xbox)        
        pub_Xbox.publish(Xbox)
        rate.sleep()


if __name__ == '__main__':
    try:
         talker()
    except rospy.ROSInterruptException:
         pass
         
         
         
