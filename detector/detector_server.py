# encoding=utf8
#Object, face, gender and age detector using Tensorflow, Keras and Pytorch.
#This version is integrated with dedicated hhtp server.
#
#author: Cataldo Cianciaruso

import sys
sys.stdout.flush        
import os
import warnings
import cv2
import numpy as np
import tensorflow as tf
execution_path = os.getcwd()
sys.path.append(os.path.join(execution_path,"detector"))
print("Loading Face Detector......")
from detector.face_detection import Face_Detector
print("Loading Emotion Detector......")
from detector.emotion_detection import Emotion_Detector
print("Loading Gender Detector......")
from detector.gender_detection import Gender_Detector
print("Loading Age Detector......")
from detector.age_detection import Age_Detector
print("All components loaded!\n")

warnings.filterwarnings("ignore")
graph=tf.get_default_graph()

class Detector_Server:


    def __init__(self):
        self._faces=[]
        self._emotions=[]
        self._face_detector=Face_Detector()
        self._emotion_detector = Emotion_Detector()
        self._gender_detector = Gender_Detector()
        self._age_detector = Age_Detector()
        

    #Predict age of the input image and return the result
    def predict_age(self, image):
        return self._age_detector.detect_age(image)

    def get_result(self):
        result="FACE"
        for i in range(len(self._faces)):
            face=self._faces[i]
            emotion=self._emotions[i]
            result+=face+"-"+emotion+","
            
        return result
   

    #Detect the faces into the input image and return a list of coordinates
    def detect_faces(self, image, threshold=0.5):
        print("\nAnalyzing faces...")
        faces, confidences=self._face_detector.detect_face(image)
        return faces, confidences


    #Detect the gender and the age of the input faces and return the result for every face in the list given
    def detect_gender_age(self, image, faces, is_gender_enabled,
                          is_age_enabled):

        global graph
        for idx, f in enumerate(faces):

            (startX, startY) = f[0], f[1]
            (endX, endY) = f[2], f[3]

            face_crop = image[startY:endY,startX:endX]

            age="undefined"
            gen="person"

            if(is_age_enabled):
                age=self.predict_age(face_crop)

            if(is_gender_enabled):
                gen = self._gender_detector.predict_gender(face_crop, graph)
            
            
            self._faces.append(str(gen[0])+"-"+str(startX)+" "+str(startY)+" "+str(endX)+" "
                      +str(endY)+"-"+str(age))

        print("done!")
        

    def detect_emotions(self, image, faces):
        print("\nAnalyzing emotions...")        
        result = self._emotion_detector.detect_emotions(image, faces)

        for x in range(0, len(result)):
            res=""
            emotions = result[x]['emotions']
            for idx, (emotion, score) in enumerate(emotions.items()):
                res+=str(score)+" ";
            self._emotions.append(res)
        
        print("done!")
     


    def detect(self, file, is_age_enabled=True, is_emotion_enabled=True,
        is_gender_enabled=True):

        self._faces=[]
        self._emotions=[]
        
        image=cv2.imdecode(np.fromstring(file, dtype=np.uint8), -1)
        faces, conf=self.detect_faces(image)
        self.detect_gender_age(image, faces, is_gender_enabled, is_age_enabled)
        self.detect_emotions(image, faces)
                


if __name__== "__main__":
    pass



