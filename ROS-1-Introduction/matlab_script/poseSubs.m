%%
rosshutdown;
rosinit; %%conexión con nodo maestro
%%
posSub = rossubscriber("/turtle1/pose","turtlesim/Pose");
pause(1);
%%rostopic list
%%
posSub.LatestMessage.X
%%[msg2,status,statustext] = receive(posSub,10);