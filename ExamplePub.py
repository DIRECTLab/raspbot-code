import roslibpy

if __name__ == '__main__':
    ros = roslibpy.Ros(host="localhost", port=9090)
    ros.run()

    talker = roslibpy.Topic(ros, '/speed', 'std_msgs/Int8')

    while ros.is_connected:
        current_speed = int(input("Set speed: "))
        talker.publish(roslibpy.Message({'data': current_speed}))

    talker.unadvertise()
    ros.terminate()
