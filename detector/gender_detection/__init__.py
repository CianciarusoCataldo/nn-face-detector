# encoding=utf8
#
#author: Cataldo Cianciaruso
#
#This component perform a gender detection on input image using Keras
#
from glob import glob
import os
import sys
import logging
import urllib.request

sys.tracebacklimit = 0

def exception_handler(exception_type, exception, traceback):
    print("Detection interrupted")
sys.__excepthook__ = exception_handler

import numpy as np
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger("tensorflow").setLevel(logging.ERROR)
from keras.models import load_model
from keras.preprocessing.image import img_to_array


execution_path = os.getcwd()
index=[1, 0]

model_path=os.path.join(os.path.join(execution_path,"models"),"gender_detection.model")
if not(os.path.isfile(model_path)):
            urllib.request.urlretrieve("https://s3.ap-south-1.amazonaws.com/arunponnusamy/pre-trained-weights/gender_detection.model", model_path)
       
gender_model=load_model(model_path)

class Gender_Detector:


    def __init__(self):

        global gender_model
        self._classes = ["man","woman"]

    def predict_gender(self, face, graph):
        global gender_model
        ind=-1
        with graph.as_default():
            face_crop = cv2.resize(np.copy(face), (96,96))
            face_crop = face_crop.astype("float") / 255.0
            face_crop = img_to_array(face_crop)
            face_crop = np.expand_dims(face_crop, axis=0)
            res=gender_model.predict(face_crop)[0]
            idx = np.argmax(res)
            ind=idx
            if (res[idx]*100<99):
                ind=int(index[ind])
        
        return self._classes[ind]
