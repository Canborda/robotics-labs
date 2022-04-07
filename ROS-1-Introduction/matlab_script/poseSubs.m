%% Reiniciar nodo maestro
rosshutdown;
rosinit;
%% Crear suscriptor
posSub = rossubscriber("/turtle1/pose","turtlesim/Pose");
pause(1);
% rostopic list
% [msg2,status,statustext] = receive(posSub,10);

%% Obtener mensaje y graficar pose
% posSub.LatestMessage.X

close all;
figure();
hold on;
grid on;
axis equal;

while (1)
    % Get pose
    pose = posSub.LatestMessage;
    x = pose.X;
    y = pose.Y;
    th = pose.Theta;
    matrix = turtle_update(x, y, th);
    % Plot current pose
    clf;
    trplot(matrix, 'rgb', 'thick', 2);
    axis([-1 12 -1 12 0 1]);
    view([45 50]);
    % Set rate
    pause(0.3);
end

function mth = turtle_update(x, y, theta)
    m = angvec2tr(theta, [0 0 1]');
    m(1,4) = x;
    m(2,4) = y;
    mth = double(m);
end