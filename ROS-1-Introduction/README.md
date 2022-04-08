# robotics_lab1
Connection to ROS with matlab and teleop keys.

## Autores

- Camilo Andrés Borda
- Edwin Alfredo Higuera

## Procedimiento

<p>Con Linux operando lanzar 2 terminales. En la primera terminal escribir el comando roscore
para iniciar el nodo maestro. <br>En la segunda terminal escribir rosrun turtlesim turtlesim node, en este momento aparece la Tortuga tal y como se muestra en la siguiente imagen.</p>

<img src="https://i.postimg.cc/zHpqHHZG/2022-04-06-19-05.png" aligne='center' width="200" height="200">

<p>A continuación se procede a lanzar una instancia de Matlab y se creo el script poseSub.m.</p>

![imagen tal](https://i.postimg.cc/nCrDtZZf/2022-04-07-07-20.png)

<p>Al correr la primera sección nos hemos conectado al modo maestro de ROS, lo cual queda evidenciado con el siguiente mensaje en command Window de Matlab.</p>

```
The value of the ROS_MASTER_URI environment variable, http://localhost:11311, will be used to connect to the ROS master.
Initializing global node /matlab_global_node_73140 with NodeURI http://eladark-Katana-GF66-11UC:39157/ and MasterURI http://localhost:11311.
```
<p>Tras correr la segunda sección se puede apreciar la creación del Publisher y el Message, de la siguiente manera. </p>

![imagen tal](https://i.postimg.cc/0r5Y8jwb/2022-04-07-07-54.png)

<p>Para finalizar se ejecuta la tercera y ultima sección del script, la cual activa el nodo Publisher, el cual envia el mensaje de velocidad lineal en x = 1, al topico /turtle1/cmd_vel, generando el siguiente comportamiento en nuestra tortuga. </p>

![imagen tal](https://i.postimg.cc/0K98Nd44/2022-04-06-19-15.png)

<p>A continuación se crea un script en Matlab llamado poseSubs.m, que permite suscribirse al tópico de pose de la simulación de turtle1.</p>





![KeyBoard](https://i.postimg.cc/RqXH8hkT/2022-04-06-23-29.png)