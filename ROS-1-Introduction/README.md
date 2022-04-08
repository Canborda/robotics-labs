# robotics_lab1
Connection to ROS with matlab and teleop keys.

## Autores

- Camilo Andrés Borda
- Edwin Alfredo Higuera

## Procedimiento

Con Linux operando lanzar 2 terminales. En la primera terminal escribir el comando roscore
para iniciar el nodo maestro, en la segunda terminal escribir rosrun turtlesim turtlesim node, en este momento aparece la Tortuga tal y como se muestra en la siguiente imagen.

<img src="images/console1.png" margin='auto' width="500" height="400">

A continuación se procede a lanzar una instancia de Matlab y se creo el script poseSub.m.

<img src="images/mat1.png" margin='auto' width="500" height="400">


Al correr la primera sección nos hemos conectado al modo maestro de ROS, lo cual queda evidenciado con el siguiente mensaje en command Window de Matlab.

```
The value of the ROS_MASTER_URI environment variable, http://localhost:11311, will be used to connect to the ROS master.
Initializing global node /matlab_global_node_73140 with NodeURI http://eladark-Katana-GF66-11UC:39157/ and MasterURI http://localhost:11311.
```
Tras correr la segunda sección se puede apreciar la creación del Publisher y el Message, de la siguiente manera. 

<img src="images/var1.png" margin='auto' width="500" height="200">

Para finalizar se ejecuta la tercera y ultima sección del script, la cual activa el nodo Publisher, el cual envia el mensaje de velocidad lineal en x = 1, al topico /turtle1/cmd_vel, generando el siguiente comportamiento en nuestra tortuga. 

<img src="images/tortuga1.png" margin='auto' width="500" height="400">



A continuación se crea un script en Matlab llamado poseSubs.m, que permite suscribirse al tópico de pose de la simulación de turtle1.



<img src="images/rqt1.png" margin='auto' width="500" height="400">

