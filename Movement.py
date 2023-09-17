from Car import Car
import time

if __name__ == '__main__':
    car = Car()
    
    car.control_car(100, 100)

    time.sleep(4)

    car.control_car(0, 0)


    car.control_car(0, 0)
