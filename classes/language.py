import numpy as np
import PIL
from PIL import ImageDraw, ImageFont, Image
import pickle

import sys
dir_path = '/home/david/GIT/cs481-senior-design/s19/'
sys.path.append(dir_path)

import LanguageModel


class Language:

    def __init__(self):
        self.predModel = self.load_lang()  #trying to load a LanguageModel type 

    def get_extension(box, img:PIL.Image):
        '''
        given a likely object; 
        crop box --> to conv-net --> lang model
        OR, if predicting, crop box --> conv-net --> retrieve prediction + lang model
        '''
        size = 224
        img_resized = img.resize(size=(size, size))    
        cleanImg = img_resized.copy();
        bottom = box[0] * 224
        left = box[1] * 224
        top = box[2] * 224
        right  = box[3] * 224
        formattedBox = (int(left), int(bottom), int(right), int(top)) # coordinates need to be corrected for crop
        croppedImg = cleanImg.crop(formattedBox)
        croppedImg.load()
        croppedImg = np.array(croppedImg) 
        extension = croppedImg[:, :, ::-1].copy()
        return extension

    def learn_word(self, robot, extensions, intensions):

        

    def predict_word(self, robot, extensions):
        preds = []
        for i in range(len(extensions)):
            currentImg = extensions.pop()
            preds.append(predModel.predictImageWord(currentImg))
        preds = [item[0] for item in preds] #remove probability number in tuple
        prediction = collections.Counter(preds).most_common(1)[0][0]
        return prediction
        # robot.say_text(prediction).wait_for_completed()

    def update_lang(self):
        with open(dir_path+'language-model.pickle', 'w') as handle:
            self.predModel.pickle(handle) #trying to save a LanguageModel type  

    def load_lang(self):
        with open(dir_path+'language-model.pickle', 'rb') as handle:
            self.predModel = pickle.load(handle) #trying to load a LanguageModel type    