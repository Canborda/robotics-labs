#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

from pynput.keyboard import Key, Listener

CURRENT_KEY = None

LINEAR_RES = 1
LINEAR_MAX = 10

ANGULAR_RES = 1
ANGULAR_MAX = 10

# Key pressed and released Callbacks

def pressed(key):
    global CURRENT_KEY
    try:
        CURRENT_KEY = key.char
    except AttributeError:
        CURRENT_KEY = key

def released(key):
    global CURRENT_KEY
    CURRENT_KEY = None

class keyop_publisher:

    def __init__(self):

        # Setup keyboard listener
        self.listener = Listener(on_press=pressed, on_release=released)
        self.listener.start()

        # Define publisher
        self.pub_velocity = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10)

        # Polling
        self.msg = Twist()
        self.rate = rospy.Rate(10) # publish messages at 10Hz

        # LOOP
        
        while not rospy.is_shutdown():

            lin = self.msg.linear.x
            ang = self.msg.angular.z

            # Exit with keyboard
            if CURRENT_KEY == Key.esc:
                break
            
            # Move X
            elif CURRENT_KEY == 'w':
                self.msg.linear.x = lin + LINEAR_RES if lin < LINEAR_MAX else LINEAR_MAX
            elif CURRENT_KEY == 's':
                self.msg.linear.x = lin - LINEAR_RES if lin > -LINEAR_MAX else -LINEAR_MAX
            
            # Rotate
            elif CURRENT_KEY == 'a':
                self.msg.angular.z = ang + ANGULAR_RES if ang < ANGULAR_MAX else ANGULAR_MAX
            elif CURRENT_KEY == 'd':
                self.msg.angular.z = ang - ANGULAR_RES if ang > -ANGULAR_MAX else -ANGULAR_MAX
            
            # Stop
            elif CURRENT_KEY == 'x':
                self.msg.linear.x = 0.0
                self.msg.angular.z = 0.0
            
            # Publish and wait
            self.pub_velocity.publish(self.msg)
            self.rate.sleep()

            if self.msg.linear.x != lin or self.msg.angular.z != ang:
                rospy.loginfo(f'>> New velocity values [linear = {self.msg.linear.x}, angular = {self.msg.angular.z}]')


if __name__ == "__main__":
    node_name = "keyop_node"
    rospy.init_node("keyop_node", anonymous=True)
    rospy.loginfo(f'>> STATUS: Node \"{node_name}\" initialized.')
    keyop_publisher()
    rospy.signal_shutdown('Request shutdown')
    rospy.loginfo(f'>> STATUS: Node \"{node_name}\" shutted down.')
    rospy.spin()