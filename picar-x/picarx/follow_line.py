import picarx_improved
import atexit
import bus
import time
import photosensor_interpreter
import concurrent.futures
import rossros

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

def simultaneous_ros(car):
    photosensor_bus = rossros.Bus(car.sensors.get_grayscale_data(), "photosensor")
    controller_bus = rossros.Bus(car.sensors.photo_interpret.check_center([3,3,3]), "follow_sensor")
    controller = FollowLine(car)
    bTerminate = rossros.Bus(0, "Termination Bus")

    # Wrap the sawtooth wave signal generator into a producer
    photo_prod = rossros.Producer(
    car.sensors.get_grayscale_data,  # function that will generate data
    photosensor_bus,  # output data bus
    0.05,  # delay between data generation cycles
    bTerminate,  # bus to watch for termination signal
    "Read sawtooth wave signal")


    controller_consume = rossros.Consumer(
    controller.follow_line,  # function that will process data
    (controller_bus),  # input data buses
    0.05,  # delay between data control cycles
    bTerminate,  # bus to watch for termination signal
    "Controller")

    # Make a timer (a special kind of producer) that turns on the termination
    # bus when it triggers
    terminationTimer = rossros.Timer(
        bTerminate,  # Output data bus
        3,  # Duration
        0.01,  # Delay between checking for termination time
        bTerminate,  # Bus to check for termination signal
        "Termination timer")  # Name of this timer

    """ Fifth Part: Concurrent execution """

    # Create a list of producer-consumers to execute concurrently
    producer_consumer_list = [controller_consume, photo_prod,
                            terminationTimer]

    # Execute the list of producer-consumers concurrently
    rossros.runConcurrently(producer_consumer_list)


if __name__ == "__main__":
    px = picarx_improved.Picarx()
    simultaneous_ros(px)
    #OLD
    # px = picarx_improved.Picarx()
    # px.maneuver_follow_line()
    # atexit.register(px.stop)
