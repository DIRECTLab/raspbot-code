import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
import time
from sensor_msgs.msg import Range


EchoPin = 18
TrigPin = 16


class SonarPublisher(Node):
  def __init__(self):
    super().__init__('sonar_publisher')
    self.publisher = self.create_publisher(Range, 'sonar', 10)
    timer_period = 0.1 # seconds between scans
    self.timer = self.create_timer(timer_period, self.timer_callback)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(EchoPin, GPIO.IN)
    GPIO.setup(TrigPin, GPIO.OUT)
  
  def timer_callback(self):
    msg = Range()
    msg.radiation_type = 0
    msg.field_of_view = 0.5235988
    msg.min_range = 0.02
    msg.max_range = 4.0
    msg.range = self.distance()
    
    self.publisher.publish(msg)


  def distance(self):
    GPIO.output(TrigPin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin, GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03:
            return -1.0
    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if (t5 - t1) > 0.03:
            return -1.0

    t2 = time.time()
    time.sleep(0.01)
    return ((t2 - t1) * 340 / 2)

def main(args=None):
  rclpy.init(args=args)
  publisher = SonarPublisher()
  rclpy.spin(publisher)
  publisher.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()