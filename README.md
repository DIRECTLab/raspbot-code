# Using the Docker Container

## Placing the ros2_nodes folder as /root/ros2_ws/src

This will make it so your files don't get deleted when the container ends

```sh
docker run -it --rm --privileged -v ${PWD}/ros2_nodes:/root/ros2_ws/src humble
```


## Info about sonar

* Power Supply :+5V DC
* Quiescent Current : <2mA
* Working Current: 15mA
* Effectual Angle: <15°
* Ranging Distance : 2cm – 400 cm/1″ – 13ft
* Resolution : 0.3 cm
* Measuring Angle: 30 degree
* Trigger Input Pulse width: 10uS TTL pulse
* Echo Output Signal: TTL pulse proportional to the distance range
* Dimension: 45mm x 20mm x 15mm