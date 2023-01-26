import time
import os
import atexit


class PhotosensorInterpreter():

    def __init__(self, light_thresh=1500, dark_thresh=500, polarity=1) -> None:
        self.l_thresh = light_thresh
        self.d_thresh = dark_thresh
        self.polarity = polarity
        
    def check_center(self, grayscale):
        left = grayscale[1] - grayscale[0]
        right = grayscale[1] - grayscale[2]

        if left >= 0 and right >= 0:
            return 0
        elif left <= right and left < self.d_thresh:
            return -1 * (min(abs(left), grayscale[1])  / grayscale[1])
        elif right > left and right < self.d_thresh:
            return min(abs(right), grayscale[1])  / grayscale[1]
        else:
            return 0
