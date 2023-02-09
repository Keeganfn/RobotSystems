import picarx_improved
import atexit
import bus
import time
import photosensor_interpreter
import concurrent.futures

class FollowLine():
    def __init__(self, car) -> None:
        self.car = car
        pass

    def follow_line(self, data):
        self.car.set_dir_servo_angle(min(30 * data, 30))
        self.car.forward(40)
        time.sleep(.1)

    def controller_consumer(self, input_bus, delay):
        while True:
            data = input_bus.read()
            self.follow_line(data)
            time.sleep(delay)


def simultaneous(car):
    photosensor_bus = bus.MessageBus()
    controller_bus = bus.MessageBus()
    controller = FollowLine(car)

    with concurrent.futures.ThreadPoolExecutor(max_workers =2) as executor:
        eSensor = executor.submit(car.sensors.photosensor_producer, photosensor_bus, .1)
        eInterpreter = executor.submit(car.sensors.photo_interpret.consumer_producer, photosensor_bus, controller_bus, .1)
        eFollow = executor.submit(controller.controller_consumer, controller_bus, .1)
    eSensor.result()
    eInterpreter.result()
    eFollow.result()
if __name__ == "__main__":
    px = picarx_improved.Picarx()
    simultaneous(px)
    #OLD
    # px = picarx_improved.Picarx()
    # px.maneuver_follow_line()
    # atexit.register(px.stop)
