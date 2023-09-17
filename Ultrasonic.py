import RPi.GPIO as GPIO
import time
from Car import Car

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
    car = Car()
    print(f"Starting: {distance()}")
    
    left = 75
    right = 75

    try:
        while True:
            if abs(distance() - 50) > 2:
                while abs(distance() - 50) > 2:
                    if distance() < 50:
                        car.control_car(-left, -right)
                    else:
                        car.control_car(left, right)
            else:
                car.control_car(0, 0)
    except:
        car.stop()


    print(f"Ending: {distance()}")
    car.stop()
