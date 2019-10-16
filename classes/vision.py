import os
dir_path = '/home/david/GIT/language-acquisition'
os.chdir(dir_path)
from classes.mask_rcnn import MaskRCNN
import matplotlib
import queue
import numpy as np
from matplotlib import pyplot as plt

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

class Sight:
    
    # imageQueue = queue.Queue(maxsize=1)

    def __init__(self, robot=''): #  imageQueue=''
        self.robot = robot
        self.imageQueue = queue.Queue(maxsize=1)
        
        obj_det_path = "/home/david/anaconda3/envs/cozmo/lib/python3.7/site-packages/tensorflow/models/research/object_detection/"
        # faster_rcnn_inception_resnet_v2_atrous_oid_v4_2018_12_12'
        MODEL_NAME = obj_det_path + 'd2s_model'
        path = MODEL_NAME + '/frozen_inference_graph.pb'
        image_dimensions = (240, 320, 3)
        self.model = MaskRCNN(path, image_dimensions)
        PATH_TO_LABELS = os.path.join(obj_det_path + 'd2s_model', 'label_map.pbtxt')
        self.category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
        pass

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def detectImages(self):
        print('Detect Images started')
        while(True):
            if(not self.imageQueue.empty()):
                try:
                    plt.clf() # We need to clear the plot so that we are not plotting every image each iteration. (If we don't we will get increasing delay)

                    img = self.imageQueue.get()
                    image_np = self.load_image_into_numpy_array(img)

                    output_dict = self.model.detect(image_np)
    #                 print(len(output_dict['detection_masks']))
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        output_dict['detection_boxes'],
                        output_dict['detection_classes'],
                        output_dict['detection_scores'],
                        self.category_index,
    #                     instance_masks=output_dict.get('detection_masks'),
                        use_normalized_coordinates=True,
                        min_score_thresh=.10,
                        line_thickness=8)

                    matplotlib.use('TkAgg')
                    plt.imshow(image_np)
                    plt.pause(0.001) # imshow needs time to plot the image. Need this to display the image

                    print('Do you want to save this image? (y for yes, s for skip):')
    #             response = sys.stdin.readline()
                    response = input()
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

    def handle_image(self, evt, obj=None, tap_count=None, **kwargs):
        try:
            if(self.imageQueue.empty()):
                self.imageQueue.put_nowait(evt.image)
        except queue.Full:
            pass

    def configure_camera(self, robot, exposure_amount, gain_amount, color):
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

#     def run_inference_for_single_image(self, image, graph):
#         with graph.as_default():
#             config = tf.ConfigProto()
#             config.gpu_options.allow_growth=True
#         #         gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.333)
#         #  tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))     

#             with tf.Session(config=config) as sess: 
#               # Get handles to input and output tensors
#                 ops = tf.get_default_graph().get_operations()
#                 all_tensor_names = {output.name for op in ops for output in op.outputs}
#                 tensor_dict = {}
#                 for key in ['num_detections', 'detection_boxes', 'detection_scores','detection_classes', 'detection_masks']:
#                     tensor_name = key + ':0'
#                     if tensor_name in all_tensor_names:
#                           tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
#                           tensor_name)
#                 if 'detection_masks' in tensor_dict:
#                 # The following processing is only for single image
#                     detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
#                     detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
#                 # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
#                     real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
#                     detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
#                     detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
#                     detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
#                         detection_masks, detection_boxes, image.shape[1], image.shape[2])
#                     detection_masks_reframed = tf.cast(
#                         tf.greater(detection_masks_reframed, 0.5), tf.uint8)
#                 # Follow the convention by adding back the batch dimension
#                     tensor_dict['detection_masks'] = tf.expand_dims(
#                         detection_masks_reframed, 0)
#                 image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

#               # Run inference
#                 output_dict = sess.run(tensor_dict,
#                         feed_dict={image_tensor: image})

#               # all outputs are float32 numpy arrays, so convert types as appropriate
#                 output_dict['num_detections'] = int(output_dict['num_detections'][0])
#                 output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.int64)
#                 output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
#                 output_dict['detection_scores'] = output_dict['detection_scores'][0]
#                 if 'detection_masks' in output_dict:
#                     output_dict['detection_masks'] = output_dict['detection_masks'][0]
#             return output_dict