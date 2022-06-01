#!/usr/bin/env python3

from numpy import array
import numpy as np
import math
from roboticstoolbox import *
from spatialmath.pose3d import *
from spatialmath.base import *

l = [145, 107, 107, 85]


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

    try:
        q = np.double([0, 0, 0, 0])

       
        q[0] = math.atan2(th[1,3], th[0,3]) #%Cálculo de articulación en radianes
        
        w = th[0:3, 3] - l[3]*th[0:3, 2] #Desacople de muñeca:
        h = round(w[2] - l[0],3)
        r = round(math.sqrt(w[0]*w[0] + w[1]*w[1]),3)
         
        q[2] =-math.acos(round(((r*r)+(h*h)-l[1]**2-l[2]**2)/(2*l[1]*l[2]), 3))
        q[1] = math.atan2(h,r) + math.atan2(l[2]*math.sin(q[2]), l[1]+l[2]*math.cos(q[2])) - math.pi/2 #Articulaciónes en radianes
        q[3] = math.atan2(th[2,2], math.sqrt((th[0,2]*th[0,2]) +(th[1,2]*th[1,2]))) - math.pi/2 - q[1] -q[2]
        k1 = math.atan2(h,r)
        k2 = math.atan2(l[2]*math.sin(q[2]), l[1]+l[2]*math.cos(q[2]))
        
        print(q)
        print(k1, k2)
        print('w ', + w)
        return q,l,h,w,k1,k2
        
        
    except ValueError:
        print("Fuera de rango")
        print(q)
        print(r,h)
        print(w)

    
calcMTH(120, 120, 30, np.pi)

def intervalo(x1, x2, step1):
    interv = np.linspace(x1, x2, step1)
    print(interv)

    return interv

intervalo(7, 25, 8)


