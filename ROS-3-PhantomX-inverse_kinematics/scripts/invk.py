import roboticstoolbox as rtb
from spatialmath import *
from spatialmath.base import *
import numpy as np

l = np.array([14.5, 10.7, 10.7, 9])
qlims = np.array([[-3*np.pi/4, 3*np.pi/4],[-3*np.pi/4, 3*np.pi/4],[-3*np.pi/4, 3*np.pi/4],[-3*np.pi/4, 3*np.pi/4]])
robot = rtb.DHRobot(
    [rtb.RevoluteDH(alpha=np.pi/2, d=l[0], qlim=qlims[0,:]),
    rtb.RevoluteDH(a=l[1], offset=np.pi/2, qlim=qlims[0,:]),
    rtb.RevoluteDH(a=l[2], qlim=qlims[0,:]),
    rtb.RevoluteDH(qlim=qlims[0,:])],
    name="Px_DH_std")
robot.tool = transl(l[3],0,0).dot(troty(np.pi/2).dot(trotz(-np.pi/2)))
print(robot)

qt = np.deg2rad(np.array([60, -80, 20, 25]))
Tt = robot.fkine(qt)

# Desacople 
np.set_printoptions(suppress=True)
T = Tt.A
Tw = T-(l[3]*T[0:4,2]).reshape(4,1)

#  Solucion q1
q1 = np.arctan2(Tw[1,3],Tw[0,3])
print(q1,np.rad2deg(q1))      

# Solucion 2R
h = Tw[2,3] - l[0]
r = np.sqrt(Tw[0,3]**2 + Tw[1,3]**2)
# Codo abajo
the3 = np.arccos((r**2+h**2-l[1]**2-l[2]**2)/(2*l[1]*l[2]))
the2 = np.arctan2(h,r) - np.arctan2(l[2]*np.sin(the3),l[1]+l[2]*np.cos(the3))
q2d = -(np.pi/2-the2)
q3d = the3

# Codo arriba
the2 = np.arctan2(h,r) + np.arctan2(l[2]*np.sin(the3),l[1]+l[2]*np.cos(the3))
q2u = -(np.pi/2-the2)
q3u = -the3

# Solucion q4
Rp = (rotz(q1).T).dot(T[0:3,0:3])
pitch = np.arctan2(Rp[2,0],Rp[0,0])
q4d = pitch - q2d - q3d
q4u = pitch - q2u - q3u

q = np.empty((2,4))
q[:] =np.NaN
q[0,:] = np.array([q1, q2u, q3u, q4u])
q[1,:] = np.array([q1, q2d, q3d, q4d])

print(q)