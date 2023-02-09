import time
import os
import atexit
from collections import deque


class PhotosensorInterpreter():

    def __init__(self, light_thresh=1500, dark_thresh=500, polarity=1) -> None:
        self.l_thresh = light_thresh
        self.d_thresh = dark_thresh
        self.polarity = polarity
        self.g1 = deque([], maxlen=5)
        self.g2 = deque([], maxlen=5)
        self.g3 = deque([], maxlen=5)
        data = deque([], maxlen=10)


    def consumer_producer(self, input_bus, output_bus, delay):
        while True:
            photosensor_msg = input_bus.read()
            response = self.check_center(photosensor_msg)
            output_bus.write(response)
            time.sleep(delay)

    def check_center(self, grayscale):
        if len(self.g1) == 0:
            self.g1.append(grayscale[0])
            self.g2.append(grayscale[1])
            self.g3.append(grayscale[2])

        curr_g1 = abs(sum(self.g1)/len(self.g1) - grayscale[0])
        curr_g2 = abs(sum(self.g2)/len(self.g2) - grayscale[1]) 
        curr_g3 = abs(sum(self.g3)/len(self.g3) - grayscale[2]) 

        print("CURRENT", [curr_g1, curr_g2, curr_g3])

        self.g1.append(grayscale[0])
        self.g2.append(grayscale[1])
        self.g3.append(grayscale[2])
        total = 0
        if curr_g1 > curr_g3:
            total = -(curr_g1)
        if curr_g1 < curr_g3:
            total = (curr_g3)
        if curr_g2 < curr_g1 and curr_g2 < curr_g3:
            total = 0


        return total


        # left = grayscale[1] - grayscale[0]
        # right = grayscale[1] - grayscale[2]

        # if left >= 0 and right >= 0:
        #     return 0
        # elif left <= right and left < self.d_thresh:
        #     return -1 * (min(abs(left), grayscale[1])  / grayscale[1])
        # elif right > left and right < self.d_thresh:
        #     return min(abs(right), grayscale[1])  / grayscale[1]
        # else:
        #     return 0
