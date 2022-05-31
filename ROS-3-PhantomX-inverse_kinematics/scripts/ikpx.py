#!/usr/bin/env python3

import rospy
import time
from std_msgs.msg import String
import numpy as np
from sensor_msgs.msg import JointState
import os, sys
from py_console import console, bgColor, textColor
from pynput.keyboard import Key, Listener
import roboticstoolbox as rtb
from spatialmath import *
from spatialmath.base import *
from spatialmath.pose3d import *

from inv import *

l = [14.5, 10.7, 10.7, 8.5]
mt = 0
qlims = np.array([[-3*np.pi/4, 3*np.pi/4],[-3*np.pi/4, 3*np.pi/4],[-3*np.pi/4, 3*np.pi/4],[-3*np.pi/4, 3*np.pi/4]])
px = rtb.DHRobot(
    [rtb.RevoluteDH(alpha=np.pi/2, d=l[0], qlim=qlims[0,:]),
    rtb.RevoluteDH(a=l[1], offset=np.pi/2, qlim=qlims[0,:]),
    rtb.RevoluteDH(a=l[2], qlim=qlims[0,:]),
    rtb.RevoluteDH(qlim=qlims[0,:])],
    name="Px_DH_std")
px.tool = transl(l[3],0,0).dot(troty(np.pi/2).dot(trotz(-np.pi/2)))
print(px)


SELECTED_JOINT = 0
JOINTS = {
    ' waist    ': 0,
    ' shoulder ': 0,
    ' elbow    ': 0,
    ' wrist    ': 0,
}
LIMITS = {
    'low': -90,
    'high': 90,
    'step': 10,
}
POSITION = {
    '1': {
        'x': 0,
        'y': 10,
        'z': 1,
        'theta':-np.pi/6,
    },
    '2': {
        'x': 0,
        'y': 10,
        'z': 10,
        'theta':-np.pi/6,
    },
    '3': {
        'x': 10,
        'y': 0,
        'z': 10,
        'theta':-np.pi/6,
    },
    '4': {
        'x': 10,
        'y': 0,
        'z': 3,
        'theta':-np.pi/6,
    },
    '5': {
        'x': 10,
        'y': 0,
        'z': 10,
        'theta':-np.pi/6,
    },
    '6': {
        'x': 0,
        'y': -10,
        'z': 10,
        'theta':-np.pi/6,
    },
    '7': {
        'x': 0,
        'y': -10,
        'z': 1,
        'theta':-np.pi/6,
    },
    '8': {
        'x': 0,
        'y': -10,
        'z': 10,
        'theta':-np.pi/6,
    },
    '9': {
        'x': 10,
        'y': 0,
        'z': 10,
        'theta':-np.pi/6,
    },
    '10': {
        'x': 10,
        'y': 0,
        'z': 4,
        'theta':-np.pi/6,
    },
}



def vectQ():
    qu = inv(mt, l)

def publishMessage():
    # Define and fill message
    state = JointState()
    state.header.stamp = rospy.Time.now()
    state.name = list(map(lambda s: s.replace(' ', ''), JOINTS.keys()))
    state.position = list(map(lambda p: p*np.pi/180, JOINTS.values()))
    # Create publisher and publish message
    pub = rospy.Publisher('/joint_states', JointState, queue_size=0)
    pub.publish(state)

def updateSelectedValue(key):
    global SELECTED_JOINT
    joint = list(JOINTS.keys())[SELECTED_JOINT]
    if key == Key.right: JOINTS[joint] = JOINTS[joint] + LIMITS['step'] if JOINTS[joint] < LIMITS['high'] else LIMITS['high']
    if key == Key.left: JOINTS[joint] = JOINTS[joint] - LIMITS['step'] if JOINTS[joint] > LIMITS['low'] else LIMITS['low']


def keyPressed(key):
    if key == Key.esc: sys.exit()
    #updateSelectedJoint(key)
    updateSelectedValue(key)
    #updateScreen()
    publishMessage()

def keyReleased(key):
    pass

if __name__ == '__main__':
    rospy.init_node('ikpx')
    console.setShowTimeDefault(False)
    #updateScreen()
    with Listener(on_press=keyPressed, on_release=keyReleased) as listener:
        listener.join()