#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import JointState

import os, sys
import numpy as np
from py_console import console, bgColor, textColor
from pynput.keyboard import Key, Listener

SELECTED_COORDINATE = 0
COORDINATES = {
    'X': 0,
    'Y': 100,
    'Z': 30,
    'θ': 0,
}
LIMITS = {
    'X': {
        'low': -100,
        'high': 100,
        'step': 2,
        'unit': 'mm',
    },
    'Y': {
        'low': 50,
        'high': 150,
        'step': 2,
        'unit': 'mm',
    },
    'Z': {
        'low': 10,
        'high': 50,
        'step': 2,
        'unit': 'mm',
    },
    'θ': {
        'low': -90,
        'high': 90,
        'step': 2,
        'unit': 'deg',
    },
}

def updateScreen(key=None):
    # Restart screen
    os.system('clear')
    # Show start message
    console.log('-'*65)
    console.log(f" Press {console.highlight('UP')} and {console.highlight('DOWN')} arrows to move between coordinates")
    console.log(f" Press {console.highlight('LEFT')} and {console.highlight('RIGHT')} arrows to change the value of selected coordinate")
    #TODO console.log(f" Press {console.highlight('1 2 3 4 5')} keys to go to predefined positions")
    console.log('-'*65)
    console.warn(f"Pressed key: {key}" if key else "Press a key!")
    console.log('-'*65)
    # Highlight selected joint
    for i in range(len(COORDINATES)):
        coordinate = list(COORDINATES.keys())[i]
        bg = bgColor.GREEN if i == SELECTED_COORDINATE else ''
        txt = textColor.GREEN if i == SELECTED_COORDINATE else textColor.WHITE
        name = console.highlight(coordinate, bgColor=bg, textColor=textColor.WHITE)
        value = console.highlight(str(COORDINATES[coordinate]), bgColor='', textColor=txt)
        console.log(f"\t{name}  {value} {LIMITS[coordinate]['unit']}")
    console.log('-'*65)

def updateSelectedCoordinate(key):
    global SELECTED_COORDINATE
    if key == Key.down: SELECTED_COORDINATE = SELECTED_COORDINATE + 1 if SELECTED_COORDINATE < len(COORDINATES) - 1 else 0
    if key == Key.up: SELECTED_COORDINATE = SELECTED_COORDINATE - 1 if SELECTED_COORDINATE > 0 else len(COORDINATES) - 1

def updateSelectedValue(key):
    global SELECTED_COORDINATE
    crd = list(COORDINATES.keys())[SELECTED_COORDINATE]
    if key == Key.right: COORDINATES[crd] = COORDINATES[crd] + LIMITS[crd]['step'] if COORDINATES[crd] < LIMITS[crd]['high'] else LIMITS[crd]['high']
    if key == Key.left: COORDINATES[crd] = COORDINATES[crd] - LIMITS[crd]['step'] if COORDINATES[crd] > LIMITS[crd]['low'] else LIMITS[crd]['low']

def publishMessage():
    # Define and fill message
    state = JointState()
    state.header.stamp = rospy.Time.now()
    state.name = list(map(lambda s: s.replace(' ', ''), COORDINATES.keys()))
    state.position = list(COORDINATES.values())
    # Create publisher and publish message
    pub = rospy.Publisher('/joint_states', JointState, queue_size=0)
    pub.publish(state)

def keyPressed(key):
    # Seek events
    if key == Key.esc: sys.exit()
    updateSelectedCoordinate(key)
    updateSelectedValue(key)
    # Run events
    updateScreen(key)
    publishMessage()

def keyReleased(key):
    pass

if __name__ == '__main__':
    # Run node
    node_name = 'px_keyop'
    rospy.init_node(node_name)
    rospy.loginfo(f'>> STATUS: Node \"{node_name}\" initialized.')
    rospy.sleep(1)
    # Disable timestamp for logger
    console.setShowTimeDefault(False)
    # Print first screen
    updateScreen()
    # Publish HOME position
    # TODO how to reach home automatically
    # Start listener
    with Listener(on_press=keyPressed, on_release=keyReleased) as listener:
        listener.join()