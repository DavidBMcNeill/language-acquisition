import sys
import os
dir_path = '/home/david/GIT/language-acquisition'
sys.path.append(dir_path)
from classes.mask_rcnn import MaskRCNN
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

sys.path.append('/home/david/GIT/cozmo-python-sdk/')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src/cozmo')
from src.cozmo.util import degrees, Angle, distance_mm, speed_mmps

class Detection:
    def __init__(self):
        obj_det_path = "/home/david/anaconda3/envs/cozmo/lib/python3.7/site-packages/tensorflow/models/research/object_detection/"
        # faster_rcnn_inception_resnet_v2_atrous_oid_v4_2018_12_12'
        MODEL_NAME = obj_det_path + 'd2s_model'
        path = MODEL_NAME + '/frozen_inference_graph.pb'
        image_dimensions = (240, 320, 3)
        self.model = MaskRCNN(path, image_dimensions)
        PATH_TO_LABELS = os.path.join(obj_det_path + 'd2s_model', 'label_map.pbtxt')
        self.category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
        self.present_obj = ''

    def obj_check(self, go_box):
        '''
        tf documentation is wrong --
        order is not: [ymin, ymax, xmin, xmax]
        order IS: [ymin, xmin, ymax, xmax]
        '''
        ymin = go_box[0]
        xmin = go_box[1]
        ymax = go_box[2]
        xmax = go_box[3]
        height = ymax - ymin
        width = xmax - xmin
        area = height * width    
        x_center = (width/2) + xmin
        y_center = (height/2) + ymin
        # the condition that determines if a bounding box contains an object
        if area > 0.08: 
            return (False, y_center, x_center) # too big
        else: 
            return (True, y_center, x_center) # just right size

    def find_best_obj(self, img_np, minimum_threshold=0.10):
        output_dict = self.model.detect(image_np)
        indices = [list(output_dict['detection_scores']).index(o) 
                                for o in output_dict['detection_scores'] 
                                if o > minimum_threshold]
        if len(indices) > 0 : 
            for i in range(len(indices)):
                boxes = [output_dict['detection_boxes'][i] for i in indices]
                b = boxes[i]
                real_obj = obj_check(b)
                if not real_obj[0]: 
                    continue
                else: 
                    classes = [output_dict['detection_classes'][i] for i in indices]
                    scores = [output_dict['detection_scores'][i] for i in indices]
                    bestObj_i = i 
                    box = boxes[bestObj_i]
                    score = scores[bestObj_i]
                    label = classes[bestObj_i]

                    self.present_obj = Object_(box, score, label)
                    return self.present_obj

    def get_current_obj(self):
        return self.present_obj

    class Object_:

        def __init__(self, box, score, label):
            self.box = box
            self.score = score
            self.label = label
