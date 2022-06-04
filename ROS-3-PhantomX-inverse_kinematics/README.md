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
```
$T=\left\lbrack \begin{array}{cccc}
\mathrm{xx} & \mathrm{yx} & \mathrm{zx} & p_x \\
\mathrm{xy} & \mathrm{yy} & \mathrm{zy} & p_y \\
\mathrm{xz} & \mathrm{yz} & \mathrm{zz} & p_z \\
0 & 0 & 0 & 1
\end{array}\right\rbrack$
```

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


<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi mathvariant="italic">w</mi><mo>=</mo><mrow><mo>[</mo><mtable columnalign="center"><mtr><mtd><mrow><msub><mrow><mi mathvariant="italic">p</mi></mrow><mrow><mi mathvariant="italic">x</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi mathvariant="italic">p</mi></mrow><mrow><mi mathvariant="italic">y</mi></mrow></msub></mrow></mtd></mtr><mtr><mtd><mrow><msub><mrow><mi mathvariant="italic">p</mi></mrow><mrow><mi mathvariant="italic">z</mi></mrow></msub></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>-</mo><mi mathvariant="normal">L4</mi><mrow><mo>[</mo><mtable columnalign="center"><mtr><mtd><mrow><mi mathvariant="normal">zx</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi mathvariant="normal">zy</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi mathvariant="normal">zz</mi></mrow></mtd></mtr></mtable><mo>]</mo></mrow><mo>=</mo><mrow><mo>[</mo><mtable columnalign="center"><mtr><mtd><mrow><mi mathvariant="normal">wx</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi mathvariant="normal">wy</mi></mrow></mtd></mtr><mtr><mtd><mrow><mi mathvariant="normal">wz</mi></mrow></mtd></mtr></mtable><mo>]</mo></mrow></mrow></math>


<img src="/assets/invpxef.png" margin='auto' width="500" height="400">

Ya con las coordenadas de la articulación de la muñeca se puede proceder a hallar q2 y q3.

## Articulaciones 2 y 3

En este punto el problema se convierte en un simple problema trigonométrico, tal y como se puede apreciar en la siguiente figura:


<img src="/assets/invkinpx2.png" margin='auto' width="500" height="400">

a continuación se procede a hallar q3, para este efecto haremos uso del teorema del coseno, resultando de la siguiente manera:

$\Theta 3=\mathrm{acos}\left(\frac{{\mathrm{wx}}^2 +{\mathrm{wz}}^2 -{\mathrm{L2}}^2 -{\mathrm{L3}}^2 }{2*\mathrm{L2}*\mathrm{L3}}\right)$

ahora para hallar q2 basta con restar el angulo β del angulo Φ, de la siguiente manera: 

$\Theta 2=\mathrm{atan}\left(\frac{\mathrm{wz}}{\mathrm{wx}}\right)-\mathrm{atan}\left(\frac{\mathrm{L3}*\sin \left(\Theta 3\right)}{\mathrm{L2}+\mathrm{L3}*\cos \left(\Theta 3\right)}\right)$

## Articulación 4

Solo nos falta hallar q4, la cual obtenemos mediante la siguiente ecuación:

$\Theta 4=\omega -\Theta 2-\Theta 3$

teniendo en cuenta que ω es la orientación deseada para nuestro efector final.

Bien, ahora esta completa la cinemática inversa de nuestro Phantom X.

## Espacio de trabajo Phantom X

En la siguiente figura se puede apreciar el espacio de trabajo del robot Phantom X.

<img src="/assets/workSpacePX.png" margin='auto' width="500" height="400">