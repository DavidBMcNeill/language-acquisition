from matplotlib import pyplot as plt
import matplotlib
import os
home_path = '/home/david/GIT/language-acquisition'
os.chdir(home_path)
# print(os.getcwd())
from mask_rcnn import MaskRCNN
#from Model import Model, draw_boxes
import cozmo
import queue
import time
import threading
import numpy as np
import sys

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
print('where is vis util?',vis_util.__file__)

obj_det_path = "/home/david/anaconda3/envs/cozmo/lib/python3.7/site-packages/tensorflow/models/research/object_detection/"
# faster_rcnn_inception_resnet_v2_atrous_oid_v4_2018_12_12'
MODEL_NAME = obj_det_path + 'd2s_model'

path = MODEL_NAME + '/frozen_inference_graph.pb'
image_dimensions = (240, 320, 3)
model = MaskRCNN(path, image_dimensions)

PATH_TO_LABELS = os.path.join(obj_det_path + 'd2s_model', 'label_map.pbtxt')

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)

def detectImages():
    print('Detect Images started')
    while(True):
        if(not imageQueue.empty()):
            try:
                plt.clf() # We need to clear the plot so that we are not plotting every image each iteration. (If we don't we will get increasing delay)

                img = imageQueue.get()
                image_np = load_image_into_numpy_array(img)
                output_dict = model.detect(image_np)

                print(image_np.shape)

                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    output_dict['detection_boxes'],
                    output_dict['detection_classes'],
                    output_dict['detection_scores'],
                    category_index,
                    # instance_masks=output_dict.get('detection_masks'),
                    use_normalized_coordinates=True,
                    min_score_thresh=.10,
                    line_thickness=8)

                matplotlib.use('TkAgg')

                plt.imshow(image_np)
                plt.pause(0.001) # imshow needs time to plot the image. Need this to display the image
 
                print('Do you want to save this image? (y for yes, s for skip):')
                response = sys.stdin.readline()
                # response = input()
                if response.strip() == 'y':
                    fileName = 'cozmo_pics/'
                    currentDT = datetime.datetime.now()
                    fileName += str(currentDT)
                    converted = img.convert()
                    converted.save(fileName, "JPEG", resolution=10)
                else:
                    continue
            
            except queue.Empty:
                pass

    
def handle_image(evt, obj=None, tap_count=None,  **kwargs):
    try:
        if(imageQueue.empty()):
            imageQueue.put_nowait(evt.image)
    except queue.Full:
        pass

def configure_camera(robot, exposure_amount, gain_amount, color):
    robot.camera.color_image_enabled = color
    # Lerp exposure between min and max times
    min_exposure = robot.camera.config.min_exposure_time_ms
    max_exposure = robot.camera.config.max_exposure_time_ms
    exposure_time = (1-exposure_amount)*min_exposure + exposure_amount*max_exposure
    # Lerp gain
    min_gain = robot.camera.config.min_gain
    max_gain = robot.camera.config.max_gain
    actual_gain = (1-gain_amount)*min_gain + gain_amount*max_gain
    robot.camera.set_manual_exposure(exposure_time, actual_gain)
    
def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_lift_height(1.0)
    exposure_amount = 0.1 # Range: [0,1]
    gain_amount = 0.9 # Range: [0,1]
    color = False
    configure_camera(robot, exposure_amount, gain_amount, color)
    robot.add_event_handler(cozmo.camera.EvtNewRawCameraImage, handle_image)
    print("Added event handler")
    while True:
        time.sleep(0.1)

#model = Model(path='../f18/data/coco2014', jpegs='../f18/train2014', bb_csv='../f18/data/coco2014/tmp/bb.csv')
imageQueue = queue.Queue(maxsize=1)
threading.Thread(target=detectImages).start()
cozmo.run_program(cozmo_program, use_viewer=True)
