import sys
dir_path = '/home/david/GIT/language-acquisition'
sys.path.append(dir_path)
from classes.vision import Vision
from classes.object import Object_, Detection
from classes.movement import Movement
from classes.emote import Emote
from classes.language import Language

import queue
import collections
import threading
import random

sys.path.append('/home/david/GIT/cozmo-python-sdk/')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src/cozmo')
from src import cozmo

class Decision():
    confidence = 0
    def __init__(self, robot):
        self.image_q = queue.Queue(maxsize=1)
        self.obj_q = queue.Queue(maxsize=1)
        self.extension_feed = collections.deque(maxlen=8)
        self.intension_feed = collections.deque(maxlen=8)

        self.robot = robot
        self.state = Collect_Input()

    class Collect_Input():
        def __init__(self):
            self.detector = Detection() # build obj det model
            # Begin gathering information from Cozmo's camera
            self.look = Vision(robot)
            self.Decision.robot.add_event_handler(cozmo.camera.EvtNewRawCameraImage, self.handle_image)  
            threading.Thread(target=self.detect_images).start()
            # Begin gathering information from microphone / keyboard
            threading.Thread(target=self.get_words.start())

        def get_words(self, input_=''):
            while True:
                if(not self.Decision.intension_feed.size()>=8):
                    # W/O ASR OR EVENT-BASED
                    word = ['red',
                            'blue',
                            'green',
                            'yellow',
                            'orange',
                            'purple']
                    user_intension = random.choice(word)
                    # or give this a shot.
                    user_intension = input()
                    self.Decision.intension_feed.append(user_intension)

        def detect_images(self):
            while True:
                if(not self.Decision.image_q.empty()):
                    try: # get img if available
                        img = self.image_q.get()
                        image_np = self.look.load_image_into_numpy_array(img)
                        if self.Decision.obj_q.empty(): # detect obj, if not already
                            best_obj = self.detector.find_best_obj(image_np)
                            self.Decision.obj_q.put_nowait(best_obj)
                            if(not self.Decision.extension_feed.size()>=8): # learn ref, if not already
                                cropped_img = self.language.get_extension(best_obj.box, img.copy())
                                self.Decision.extension_feed.append(cropped_img)
                    except queue.Empty:
                        pass

        def handle_image(self, evt, obj=None, tap_count=None, **kwargs):
            try:
                if(self.Decision.image_q.empty()): 
                    self.Decision.image_q.put_nowait(evt.image)
            except queue.Full:
                pass

    class Action:

        def __init__(self, choice=0):
            # state conditions / rules 
            # .../ pre-conditions to certain actions
            self.heard_word=False
            self.learned_word=False
            self.found_obj=False
            self.reached_obj=False

            # num images of obj
            # times heard word
            # times said word

            self.move = Movement()
            self.emote = Emote()
            self.language = Language() # load LanguageModel

        def choose(self):
            list_of_functions=['go_to_object', 
                                'find_object',
                                'find_face',
                                'gesture',
                                'learn_word',
                                'predict_word',
                                'emote']

            # until Q-learning dictates what this is
            choice = random.choice(list_of_functions)

            if choice == 'predict_word':
                if self.heard_word and self.learned_word:
                    self.language.predict_word(robot, extension_feed)
            
            elif choice == 'learn_word':
                if self.heard_word: 
                    self.language.learn_word(robot, extension_feed, intension_feed)
            
            elif choice == 'go_to_object':
                if self.found_obj:
                    self.move.go_to_object(robot)

            elif choice == 'gesture':
                if self.found_obj and self.reached_obj:
                    self.move.gesture(robot)
            
            elif choice == 'find_object':
                find_object(robot)

            elif choice == 'find_face':
                self.move.find_face(robot)
            
            elif choice == 'emote':
                emotional_display = self.emote.display()
                robot.play_anim(emotional_display[0]).wait_for_completed()

        def find_object(self):
            print('Find objects started')
            looking = True
            while looking:
                if self.Decisionobj_q.empty():
                    self.found_obj=False
                    self.Decision.robot.drive_wheels(l_wheel_speed=-10, r_wheel_speed=10)
                else:
                    self.found_obj=True
                    self.Decision.robot.stop_all_motors()
                    self.Decision.robot.wait_for_all_actions_completed()
                    looking = False