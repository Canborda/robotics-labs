#!/usr/bin/env python3

from numpy import array
import numpy as np
import math
from roboticstoolbox import *
from spatialmath.pose3d import *

l = [14.5, 10.7, 10.7, 8.5]

x=8
y=10
z=2
theta=-np.pi/8

def calcMTH(x, y, z, theta):
    rz = math.rotz(math.atan2(y,x))#Cálculo MTH
    ry = math.roty(theta)
    #th =  np.zeros([4,4])
    th = rz*ry
    th[0,3] = x
    th[1,3] = y
    th[2,3] = z
    th[3,3] = 1

    print(th)
    return th

def inv(th):

    try:
        q = np.double(0, 0, 0, 0)

       
        q[0] = math.atan2(th[1,3], th[0,3]) #%Cálculo de articulación en radianes
        
        Pos_w = th[0:3, 3] - l[3]*th[0:3, 2] #Desacople de muñeca:
        h = round(Pos_w[2] - l[0],3)
        r = round(math.sqrt(Pos_w[0]*Pos_w[0] + Pos_w[1]*Pos_w[1]),3)
         
        q[2]= -q[0,2]
        q[1] = math.atan2(h,r) + math.atan2(l[2]*math.sin(q[0,2]), l[1]+l[2]*math.cos(q[0,2]))#Articulaciónes en radianes
        q[1] = q[1] - math.pi/2;   
        ang = math.atan2(th[2,2], math.sqrt((th[0,2]*th[0,2]) +(th[1,2]*th[1,2]))) - math.pi/2
        q[3] = ang - q[1] -q[2]

        return q
        print(q)
        
    except ValueError:
        print("Fuera de rango")
    