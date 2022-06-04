## robotics_lab3

# BASIC PICK AND PLACE OPERATION WITH PHANTOMX AND ROS

This repository shows how to connect and teleoperate a Phantom X robot with ROS using inverse kinematics.

> ## Authors
>
> - Camilo Andrés Borda Gil
> - Edwin Alfredo Higuera Bustos

<br>

---

<br>

El modelo cinemático inverso de un robot es un método que nos permite hallar las posiciones articulares del mismo, a partir de la posición y orientación del efector final.
Continuando con la dinámica seguida en clase, se propone obtener la cinemática inversa del robot Phantom X, la idea es obtener los valores necesarios en cada una de las cuatro juntas del robot, con el fin de conseguir la pose deseada para el efector final.
La forma más utilizada para calcular la cinemática inversa de manipuladores sencillos como el Phantom X, es el método geométrico, el cual consiste en hallar una función para cada una de sus posiciones articulares, basada en las diferentes configuraciones que el robot pueda llegar a adoptar.

## Articulación 1

<img src="/assets/q1.png" margin='auto' width="500" height="400">

Esta articulación es la mas sencilla de obtener, Ya que, como se puede apreciar en figura anterior, al tener la posición del efector final, se puede utilizar sus coordenadas en X y Y de la siguiente manera:


```
θ1 = atan (py/px)

```

## Desacople de muñeca

Con el fin de simplificar el sistema y así lograr un desarrollo mas sencillo de la cinemática inversa, se procede a utilizar un método conocido como desacople cinemático, este método nos permite resolver tres ejes de libertad de manera independiente, 
básicamente lo que se debe hacer es hallar las coordenadas de la articulación 4 (j4), la cual corresponde a la muñeca del PhantomX. 
<br>
Ya que tenemos las coordenadas del efector final y por ende tenemos la MTH del mismo, la cual resulta ser:

$T=\left\lbrack \begin{array}{cccc}
\mathrm{xx} & \mathrm{yx} & \mathrm{zx} & p_x \\
\mathrm{xy} & \mathrm{yy} & \mathrm{zy} & p_y \\
\mathrm{xz} & \mathrm{yz} & \mathrm{zz} & p_z \\
0 & 0 & 0 & 1
\end{array}\right\rbrack$

es posible hallar la posición de la muñeca (w), mediante la siguiente ecuación:

$w=\left\lbrack \begin{array}{c}
p_x \\
p_y \\
p_z 
\end{array}\right\rbrack -\mathrm{L4}\left\lbrack \begin{array}{c}
\mathrm{zx}\\
\mathrm{zy}\\
\mathrm{zz}
\end{array}\right\rbrack =\left\lbrack \begin{array}{c}
\mathrm{wx}\\
\mathrm{wy}\\
\mathrm{wz}
\end{array}\right\rbrack$

Ya con las coordenadas de la articulación de la muñeca se puede proceder a hallar q2 y q3.

## Articulaciones 2 y 3

<img src="../assets/invpxef.png" margin='auto' width="500" height="400">

<img src="../assets/invkinpx2.png" margin='auto' width="500" height="400">

<img src="../assets/workSpacePX.png" margin='auto' width="500" height="400">