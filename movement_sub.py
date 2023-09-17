import roslibpy
from Car import Car

if __name__ == '__main__':
    car = Car()
    
    client = roslibpy.Ros(host="localhost", port=9090)
    client.run()
    
    if client.is_connected:
        print("Connection to ROS successful")

    listener = roslibpy.Topic(client, '/speed', 'std_msgs/Int8')
    listener.subscribe(lambda speed_command: car.control_car(speed_command['data'], speed_command['data']))

    print("Listening for speed commands")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.terminate()
        car.stop()
