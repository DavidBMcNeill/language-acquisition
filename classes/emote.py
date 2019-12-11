import random

class Emote:

    def __init__(self):
        self.confusion_anims = [('anim_dizzy_reaction_soft_02', '9DAaXwinFdg', 9),
            ('anim_dizzy_reaction_medium_03', '9gwXd4VCK4o', 9),
            ('anim_dizzy_shake_stop_01', '6fE-4vv7g6U', 9),
            ('anim_keepaway_fakeout_02', 'MX6RrSHrv6E', 8),
            ('anim_dizzy_reaction_medium_01', 'uCnRvN8LChg', 8),
            ('anim_dizzy_reaction_medium_02', '43lIwWW0a6w', 7),
            ('anim_workout_lowenergy_getout_01', 'Mvy-MU80z48', 6),
            ('anim_launch_firsttimewakeup_helloplayer_head_angle_-20', 'GSNeqfQMN7Q', 5),
            ('anim_keepalive_eyesonly_loop_02', 'fpliwsnS5BA', 5),
            ('anim_energy_idlel2_05', 'xmf7RGlJanM', 5),
            ('anim_dizzy_reaction_soft_03', 'wW6irtD-vTs', 5)]
        self.understanding_anims = [('anim_energy_cubeshakelvl1_03', 'aBov1khHOMw', -9),
            ('anim_reacttocliff_pickup_01', 'nGGheI60fPM', -8),
            ('anim_fistbump_success_02', 'ILgKYsZfd2U', -7),
            ('anim_rtpmemorymatch_yes_01', 'QliwkU0oAdU', -7),
            ('anim_workout_mediumenergy_getready_01', '07rmab3ic70', -7),
            ('anim_explorer_huh_01_head_angle_10', 'Y9d_LGO7IWE', -6),
            ('anim_rtpmemorymatch_yes_02', 'CSmmqCly6P8', -6),
            ('anim_freeplay_reacttoface_identified_03_head_angle_40', '5tg4OFo7KOk', -5),
            ('anim_freeplay_reacttoface_identified_01_head_angle_40', 'o4-BzbvJXws', -5),
            ('anim_workout_highenergy_getready_01', 'B_I9y_tb0jY', -5)]

    def emote_confusion(self, valence=0):
        # add a parameter to enable more fine-tuned selection of animation...
        # ... depending on magnitude of valence
        return random.choice(confusion_anims)
    
    def emote_understanding(self, valence=0):
        # add a parameter to enable more fine-tuned selection of animation...
        # ... depending on magnitude of valence
        return random.choice(understanding_anims)

    def display(self, i=0):
        if i == 0:
            valence = random.choice([-1,1])
        else:
            valence = i
        display = ''
        if valence < 0:
            print('confused')
            display = emote_confusion()
        else:
            print('understanding')
            display = emote_understanding()
        return display