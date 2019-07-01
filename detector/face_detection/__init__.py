import os
import sys
import logging

import cv2
import numpy as np

execution_path = os.getcwd()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger("tensorflow").setLevel(logging.ERROR)

class Face_Detector:
    """This class define the structure of Face Detector component.
    It can detect and return the coordinates of human face into images"""
    
    def __init__(self, ptxt=os.path.join(execution_path, os.path.join("models", "deploy.prototxt")), caffm=os.path.join(execution_path,os.path.join("models", "res10_300x300_ssd_iter_140000.caffemodel"))):

        if not((os.path.isfile(ptxt))or(os.path.isfile(caffm))):
            print("Invalid model files for Face Detector. Detection Interrupted")
            sys.exit(1)
                                      
        self.prototxt=ptxt
        self.caffemodel=caffm
        
    
    def detect_face(self, image, threshold=0.5):

        """Analyze the input image and detect all the faces into it.
        After that, it returns a list of coordinates, for every face detected."""

        if image is None:
            return None
        # read pre-trained wieights
        net = cv2.dnn.readNetFromCaffe(self.prototxt, self.caffemodel)
        (h, w) = image.shape[:2]

        # preprocessing input image
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300,300)), 1.0, (300,300), (104.0,177.0,123.0))
        net.setInput(blob)

        # apply face detection
        detections = net.forward()

        faces = []
        confidences = []

        # loop through detected faces
        for i in range(0, detections.shape[2]):
            conf = detections[0,0,i,2]

            # ignore detections with low confidence
            if conf < threshold:
                continue

            # get corner points of face rectangle
            box = detections[0,0,i,3:7] * np.array([w,h,w,h])
            (startX, startY, endX, endY) = box.astype('int')
            
            faces.append([startX, startY, endX, endY])
            confidences.append(conf)

        # return all detected faces and
        # corresponding confidences
        return faces, confidences
