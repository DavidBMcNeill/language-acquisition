import cozmo
import queue
import threading
import time
from classes.vision import Vision

def cozmo_program(robot: cozmo.robot.Robot):

    imageQueue = queue.Queue(maxsize=1)
    look = Vision(robot) # , imageQueue
    
    look.configure_camera(robot, exposure_amount, gain_amount, color)
    look.robot.add_event_handler(cozmo.camera.EvtNewRawCameraImage, look.handle_image)
    
    threading.Thread(target=look.detectImages).start() # , args=(imageQueue)
    print("Added event handler")
    while True:
        time.sleep(0.1)


# threading.Thread(target=look.detectImages).start()
cozmo.run_program(cozmo_program, use_viewer=True)
