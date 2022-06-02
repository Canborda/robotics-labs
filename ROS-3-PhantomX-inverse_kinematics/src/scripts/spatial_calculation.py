#!/usr/bin/env python3

import math
import numpy as np
from spatialmath.base import *

POSITION = {
    '1': {
        'x': 0,
        'y': 14,
        'z': 1,
        'theta': np.pi,
        'gripper': False,
    },
    '2': {
        'x': 0,
        'y': 14,
        'z': 1,
        'theta': np.pi,
        'gripper': True,
    },
    '3': {
        'x': 0,
        'y': 14,
        'z': 10,
        'theta': np.pi,
        'gripper': True,
    },
    '4': {
        'x': 14,
        'y': 0,
        'z': 10,
        'theta': np.pi,
        'gripper': True,
    },
    '5': {
        'x': 14,
        'y': 0,
        'z': 3,
        'theta': np.pi,
        'gripper': True,
    },
    '6': {
        'x': 14,
        'y': 0,
        'z': 3,
        'theta': np.pi,
        'gripper': False,
    },
    '7': {
        'x': 14,
        'y': 0,
        'z': 10,
        'theta': np.pi,
        'gripper': False,
    },
    '8': {
        'x': 0,
        'y': -14,
        'z': 10,
        'theta': np.pi,
        'gripper': False,
    },
    '9': {
        'x': 0,
        'y': -14,
        'z': 1,
        'theta': np.pi,
        'gripper': False,
    },
    '10': {
        'x': 0,
        'y': -14,
        'z': 1,
        'theta': np.pi,
        'gripper': True,
    },
    '11': {
        'x': 0,
        'y': -14,
        'z': 10,
        'theta': np.pi,
        'gripper': True,
    },
    '12': {
        'x': 14,
        'y': 0,
        'z': 10,
        'theta': np.pi,
        'gripper': True,
    },
    '13': {
        'x': 14,
        'y': 0,
        'z': 4,
        'theta': np.pi,
        'gripper': True,
    },
    '14': {
        'x': 14,
        'y': 0,
        'z': 4,
        'theta': np.pi,
        'gripper': False,
    },
}

L = [145, 107, 107, 85]

def inverseKinematics(x, y, z, theta):
    rz = trotz(math.atan2(y, x))
    ry = troty(theta)

    th = np.matmul(rz, ry)
    th[0, 3] = x
    th[1, 3] = y
    th[2, 3] = z
    th[3, 3] = 1

    try:
        q = np.double([0, 0, 0, 0])

        # Cálculo de articulación en radianes
        q[0] = math.atan2(th[1, 3], th[0, 3])

        w = th[0:3, 3] - L[3]*th[0:3, 2]  # Desacople de muñeca:
        h = round(w[2] - L[0], 3)
        r = round(math.sqrt(w[0]*w[0] + w[1]*w[1]), 3)

        q[2] = - \
            math.acos(round(((r*r)+(h*h)-L[1]**2-L[2]**2)/(2*L[1]*L[2]), 3))
        q[1] = math.atan2(h, r) + math.atan2(L[2]*math.sin(q[2]), L[1] +
                                             L[2]*math.cos(q[2])) # Articulaciónes en radianes
        q[3] = math.atan2(th[2, 2], math.sqrt(
            (th[0, 2]*th[0, 2]) + (th[1, 2]*th[1, 2]))) - math.pi/2 - q[1] - q[2]
        # k1 = math.atan2(h, r)
        # k2 = math.atan2(l[2]*math.sin(q[2]), l[1]+l[2]*math.cos(q[2]))

        return True, q

    except ValueError:
        # print("ERROR! Pose out of range")
        # print('q:', q)
        # print('r:', r)
        # print('h:', h)
        # print('w:', w)
        return False, q


_, ang = inverseKinematics(120, 120, 30, np.pi)

print(ang)
print(ang*180/np.pi)


def intervalo(x1, x2, step1):
    interv = np.linspace(x1, x2, step1)
    print(interv)

    return interv


# intervalo(7, 25, 8)
