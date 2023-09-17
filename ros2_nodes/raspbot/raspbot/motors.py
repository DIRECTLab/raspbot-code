import rclpy
from rclpy.node import Node

from std_msgs.msg import Int32MultiArray
import smbus
import time
import math

class Car:
    def __init__(self):
        self._addr = 0x16
        self._device = smbus.SMBus(1)

    def __write_u8(self, register, data):
        try:
            self._device.write_byte_data(self._addr, register, data)
        except:
            print('write_u8 error')

    def __write_register(self, register):
        try:
            self._device.write_byte(self._addr, register)
        except:
            print('write_register error')

    def __write_array(self, register, data):
        try:
            self._device.write_i2c_block_data(self._addr, register, data)
        except:
            print('write_array error')

    def control_car(self, left, right):
        """
        left: int (-255, 255)
        right: int (-255, 255)

        sets the motor with the speed given (not actually in unit, just a power amount)
        """
        register = 0x01
        left_direction = 0 if left < 0 else 1
        right_direction = 0 if right < 0 else 1

        if left < 0:
            left *= -1
        if right < 0:
            right *= -1

        data = [left_direction, left, right_direction, right]
        self.__write_array(register, data)

    def stop(self):
        register = 0x02
        self.__write_u8(register, 0x00)

    def set_servo(self, servo_id, angle):
        register = 0x03
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        data = [servo_id, angle]
        self.__write_array(register, data)


class MinimalSubscriber(Node):
  def __init__(self):
    super().__init__('motors')
    self.car = Car()
    self.motor_subscription = self.create_subscription(Int32MultiArray, '/motor_control', self.motor_callback, 10)
    self.servo_subscription = self.create_subscription(Int32MultiArray, '/servo_control', self.servo_callback, 10)
    self.servo1_angle = -1
    self.servo2_angle = -1
  
  def motor_callback(self, msg):
    self.car.control_car(msg.data[0], msg.data[1])
  
  def servo_callback(self, msg):
    if msg.data[0] != self.servo1_angle:
      self.car.set_servo(1, msg.data[0])
      self.servo1_angle = msg.data[0]
    if msg.data[1] != self.servo2_angle:
      self.car.set_servo(2, msg.data[1])
      self.servo2_angle = msg.data[1]

def main(args=None):
  rclpy.init(args=args)
  
  subscriber = MinimalSubscriber()
  
  try:
    rclpy.spin(subscriber)
  except Exception as e:
    print(e)
    subscriber.car.stop()
  
  subscriber.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
  main()