import sys
# customize path according to where sdk repo is in your system
sdk_path = '/home/david/GIT/cozmo-python-sdk/examples/tutorials/03_vision/'
sys.path.append(sdk_path)
from face_follow import follow_faces

dir_path = '/home/david/GIT/language-acquisition'
sys.path.append(dir_path)
from classes.object import Object_

sys.path.append('/home/david/GIT/cozmo-python-sdk/')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src')
sys.path.append('/home/david/GIT/cozmo-python-sdk/src/cozmo')
from src import cozmo
from src.cozmo.util import degrees, Angle, distance_mm, speed_mmps

class Movement():

    def __init__(self):
        self.object_

    def reorient(self, go_box):
        real_obj = self.object_.obj_check(go_box)    
        x_center = real_obj[2]
        y_center = real_obj[1]
        print('y:', y_center, 'x:', x_center)
        if not real_obj[0]: # break 'go_to' loop
            drive_dist = 1000 
            turn_angle = 1000
        else:
            # we want x_center to be 0.5, turn right -> (-) / turn left -> (+)
            if x_center > 0.56 or x_center < 0.44:
                x_diff = x_center - 0.5
                turn_angle = (x_diff * (-50)) / 2 
            else: turn_angle = 0 # break 'go_to' loop
            # we want y-center to be = 0.42, (-) -> backwards, (+) -> forwards   
            if y_center > 0.48 or y_center < 0.36:
                y_diff = y_center - 0.42
                # need to account for parallax -- things far away approach slowly; things close up approach quickly
                base = y_diff * (-10)
                drive_dist = np.power(base,4)
            else: drive_dist = 0 # break 'go_to' loop
        return drive_dist, turn_angle

    def find_object(self, robot):
        print('Find objects started')
        robot.set_lift_height(1.0).wait_for_completed()
        robot.set_head_angle(cozmo.robot.MIN_HEAD_ANGLE).wait_for_completed()

        find=True
        drive, turn = self.go_to_obj(robot, obj.box)
        if drive == 0 and turn == 0:  
            print('Object reached!')
            # predict(robot)
            predict = True
            understanding = True
            find = False
        else: #drive == 1000 and turn == 1000
            print('go to object failed') 
            # predict(robot)
            # emote CONFUSED
            confused = True
            predict = False
            pass

    def go_to_object(self, robot, box):
        last_drive = 1000
        last_turn = 1000
        while True:
            print("go to ", box)
            drive_dist, turn_angle = self.reorient(box)
            print('turned ', turn_angle, 'degrees', '/ drove', drive_dist,'mm')
            
            # these conditions break 'go_to' loop
            if drive_dist > last_drive: break
            elif turn_angle > last_turn: break
            if turn_angle == 0 and drive_dist == 0: break
            robot.turn_in_place(degrees(turn_angle),in_parallel=False)
            robot.wait_for_all_actions_completed()  
            last_turn = turn_angle
            
            robot.drive_straight(distance_mm(drive_dist), speed_mmps(40), should_play_anim=False, in_parallel=False)
            last_drive = drive_dist
            robot.wait_for_all_actions_completed()  
        print('Stop going to object')
        return drive_dist, turn_angle 

    def find_face(self, robot):
        cozmo.run_program(follow_faces) # , use_viewer=True, force_viewer_on_top=True

    def gesture(self, robot):
