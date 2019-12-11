import sys
import os
dir_path = '/home/david/GIT/language-acquisition'
sys.path.append(dir_path)
import matplotlib
import queue
import numpy as np
from matplotlib import pyplot as plt

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

sys.path.append('/home/david/GIT/cozmo-python-sdk/')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src/cozmo')
from src.cozmo.util import degrees, Angle, distance_mm, speed_mmps


class Vision:

    def __init__(self, robot=''): #  imageQueue=''
        self.robot = robot
        self.robot.set_lift_height(1.0)
        self.exposure_amount = 0.1 # Range: [0,1]
        self.gain_amount = 0.9 # Range: [0,1]
        self.color = False
        self.configure_camera(robot, exposure_amount, gain_amount, color)
        pass

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def configure_camera(self, robot, exposure_amount, gain_amount, color):
        self.robot.camera.color_image_enabled = color
        # Lerp exposure between min and max times
        min_exposure = robot.camera.config.min_exposure_time_ms
        max_exposure = robot.camera.config.max_exposure_time_ms
        exposure_time = (1-exposure_amount)*min_exposure + exposure_amount*max_exposure
        # Lerp gain
        min_gain = robot.camera.config.min_gain
        max_gain = robot.camera.config.max_gain
        actual_gain = (1-gain_amount)*min_gain + gain_amount*max_gain
        self.robot.camera.set_manual_exposure(exposure_time, actual_gain) 


#     def detect_images(self, img):
        
#         print('Detect Images started')
#         img = self.imageQueue.get()
#         image_np = self.load_image_into_numpy_array(img)

#         output_dict = self.model.detect(image_np)
# #                 print(len(output_dict['detection_masks']))
#         return output_dict

#     def handle_image(self, evt, obj=None, tap_count=None, **kwargs):
#         try:
#             if(self.imageQueue.empty() and not self.robot.is_moving):
#                 self.imageQueue.put_nowait(evt.image)
#         except queue.Full:
#             pass
