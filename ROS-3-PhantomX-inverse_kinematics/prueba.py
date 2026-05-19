
#!/usr/bin/env python3

from numpy import array
import numpy as np
import math
from roboticstoolbox import *
from spatialmath.pose3d import *
from spatialmath.base import *

l = [14.5, 10.7, 10.7, 8.5]

x=8
y=10
z=2
theta=-np.pi/8

def calcMTH(x, y, z, theta):
    rz = trotz(math.atan2(y,x))#Cálculo MTH
    ry = troty(theta)
    print(ry.shape)
    print(rz)
    print(theta)
    print(ry)
    #th =  np.zeros([4,4])
    th = np.matmul(rz,ry) 
    th[0,3] = x
    th[1,3] = y
    th[2,3] = z
    th[3,3] = 1
    print(th)

    return th
    
calcMTH(8, 10, 2, -np.pi/8)