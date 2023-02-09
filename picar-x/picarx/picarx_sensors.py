import time
import os
import photosensor_interpreter

try :
    from robot_hat import *
    from robot_hat import reset_mcu
    reset_mcu()
    time.sleep(0.01)
except ImportError :
    print (" This computer does not appear to be a PiCar - X system (robot_hat is not present ) . Shadowing hardware calls with substitute functions ")
    from sim_robot_hat import *

class PicarxSensors():

    def __init__(self, grayscale_pins, ultrasonic_pins) -> None:   
        self.adc0, self.adc1, self.adc2 = grayscale_pins
        self.grayscale = Grayscale_Module(self.adc0, self.adc1, self.adc2, reference=1000)
        # ultrasonic init
        # usage: distance = self.ultrasonic.read()
        tring, echo= ultrasonic_pins
        self.ultrasonic = Ultrasonic(Pin(tring), Pin(echo))
        self.photo_interpret = photosensor_interpreter.PhotosensorInterpreter(1500, 500, 1)


    def photosensor_producer(self, output_bus, delay):
        while True:
            output_bus.write(self.get_grayscale_data)
            time.sleep(delay)

    def get_distance(self):
        return self.ultrasonic.read()

    def set_grayscale_reference(self, value):
        self.get_grayscale_reference = value
        
    def get_grayscale_data(self):
        return list.copy(self.grayscale.get_grayscale_data())