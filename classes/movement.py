import sys
# customize path according to where sdk repo is in your system
sdk_path = '/home/david/GIT/cozmo-python-sdk/examples/tutorials/03_vision/'
sys.path.append(sdk_path)
from face_follow import follow_faces

sys.path.append('/home/david/GIT/cozmo-python-sdk/')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src/cozmo')
from src import cozmo

print(sys.path)

cozmo.run_program(follow_faces, use_viewer=True, force_viewer_on_top=True)
# class Move:


#     def __init__(self,robot=''):

#         self.robot=robot