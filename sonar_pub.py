import roslibpy
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

EchoPin = 18
TrigPin = 16

GPIO.setmode(GPIO.BOARD)

GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TrigPin, GPIO.OUT)

def distance():
    GPIO.output(TrigPin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin, GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03:
            return -1
    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if (t5 - t1) > 0.03:
            return -1

    t2 = time.time()
    time.sleep(0.01)
    return ((t2 - t1) * 340 / 2) * 100

if __name__ == '__main__':
    ros = roslibpy.Ros(host="localhost", port=9090)
    ros.run()

    talker = roslibpy.Topic(ros, '/sonar', 'std_msgs/Float32')

    while ros.is_connected:
        time.sleep(1/15)
        current_distance = distance()
        talker.publish(roslibpy.Message({'data': current_distance}))

    talker.unadvertise()
    ros.terminate()
