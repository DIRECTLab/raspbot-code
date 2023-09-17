from picamera2 import Picamera2
import time
import roslibpy
import base64

if __name__ == '__main__':
    ros = roslibpy.Ros(host="localhost", port=9090)
    ros.run()

    talker = roslibpy.Topic(ros, '/camera/image/compressed', 'sensor_msgs/CompressedImage')
    
    picam2 = Picamera2()
    picam2.start()
    
    print("starting publishing")
    while ros.is_connected:
        img = picam2.capture_array()
        encoded = base64.b64encode(img).decode('ascii')
        talker.publish(dict(format='jpeg', data=encoded))
        time.sleep(1/15)

    talker.unadvertise()
    ros.terminate()
