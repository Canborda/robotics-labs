#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

import numpy as np

from spatial_calculation import inverseKinematics

def callback(data):
    # Unpack data
    x = data.linear.x
    y = data.linear.y
    z = data.linear.z
    theta = data.angular.z*np.pi/180
    # Get joint angles
    success, q = inverseKinematics(x, y, z, theta)
    # Publish angles to Rviz
    if (success):
        state = JointState()
        state.header.stamp = rospy.Time.now()
        state.name = ['waist', 'shoulder', 'elbow', 'wrist']
        state.position = q
        # Create publisher and publish message
        pub = rospy.Publisher('/joint_states', JointState, queue_size=0)
        pub.publish(state)
    else:
        print('Out of range', q)


def listener():
    # Run node
    node_name = 'pose2joints_translator'
    rospy.init_node(node_name)
    rospy.loginfo(f'>> STATUS: Node \"{node_name}\" initialized.')
    # Subscribe to POSE topic
    rospy.Subscriber("/effector_pose", Twist, callback)
    # Hold rosnode
    rospy.spin()


if __name__ == '__main__':
    try:
        while not rospy.is_shutdown():
            listener()
    except rospy.ROSInterruptException:
        pass