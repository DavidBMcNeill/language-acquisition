import cozmo
import queue
import threading
import time
from classes.vision import Sight

def cozmo_program(robot: cozmo.robot.Robot):
    robot.set_lift_height(1.0)
    exposure_amount = 0.1 # Range: [0,1]
    gain_amount = 0.9 # Range: [0,1]
    color = False
    
    imageQueue = queue.Queue(maxsize=1)
    look = Sight(robot) # , imageQueue
    
    look.configure_camera(robot, exposure_amount, gain_amount, color)
    look.robot.add_event_handler(cozmo.camera.EvtNewRawCameraImage, look.handle_image)
    
    threading.Thread(target=look.detectImages).start() # , args=(imageQueue)
    print("Added event handler")
    while True:
        time.sleep(0.1)


# threading.Thread(target=look.detectImages).start()
cozmo.run_program(cozmo_program, use_viewer=True)
