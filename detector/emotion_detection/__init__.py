#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import logging
import sys
#sys.tracebacklimit = 0

def exception_handler(exception_type, exception, traceback):
    print("Detection interrupted")

sys.__excepthook__ = exception_handler
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.ERROR)

import cv2
import numpy as np
import tensorflow as tf
import urllib.request

tf.logging.set_verbosity(tf.logging.ERROR)

from keras.models import load_model

from emotion_detection.exceptions import InvalidImage

execution_path = os.getcwd()
class Emotion_Detector(object):
    """
    Allows performing detection of emotions on faces
    """

    
    
    def __init__(self, emotion_model=os.path.join(execution_path,os.path.join("models", "emotion_model.hdf5")),
                 cascade_file: str = None,
                 scale_factor: float = 1.3,
                 offsets: tuple = (20, 40),
                 compile: bool = False):
        """
        Initializes the face detector and Keras model for emotion detection.
        :param cascade_file: file URI with the Haar cascade for face classification
        :param emotion_model: file URI with the Keras hdf5 model
        :param scale_factor: parameter specifying how much the image size is reduced at each image scale
        :param min_face_size: minimum size of the face to detect
        :param offsets: padding around face before classification
        :param compile: value for Keras `compile` argument
        """        
        self.__scale_factor = scale_factor
        self.__offsets = offsets
        self.__labels={
            0: 'angry',
            1: 'disgust',
            2: 'fear',
            3: 'happy',
            4: 'sad',
            5: 'surprise',
            6: 'neutral'
        }
        
        cascade_file=os.path.join(execution_path ,os.path.join("models","haarcascade_frontalface_default.xml"))            
        
        self.__face_detector = cv2.CascadeClassifier(cascade_file)

        # Local Keras model
        self.deployment = False
        config = tf.ConfigProto(log_device_placement=False)
        config.gpu_options.allow_growth = True
        self.__emotion_classifier = load_model(emotion_model, compile=compile)
        self.__emotion_classifier._make_predict_function()
        self.__emotion_target_size = self.__emotion_classifier.input_shape[
                1:3]
        

    @staticmethod
    def pad(image):
        row, col = image.shape[:2]
        bottom = image[row - 2:row, 0:col]
        mean = cv2.mean(bottom)[0]

        bordersize = 40
        padded_image = cv2.copyMakeBorder(
            image,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[mean, mean, mean])
        return padded_image


    @staticmethod
    def __preprocess_input(x, v2=True):
        x = x.astype('float32')
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x


    def __apply_offsets(self, face_coordinates):
        x, y, width, height = face_coordinates
        x_off, y_off = self.__offsets
        return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)
    

    def detect_emotions(self, img, face_rectangles) -> list:
        """
        Detects bounding boxes from the specified image with ranking of emotions.
        :param img: image to process
        :param face_rectangles: list of coordinates of faces
        :return: list containing all the bounding boxes detected with their emotions.
        """
        if img is None or not hasattr(img, "shape"):
            raise InvalidImage("Image not valid.")

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        emotions = []
        for temp, face_coordinates in enumerate(face_rectangles):
            (startX, startY) = face_coordinates[0], face_coordinates[1]
            (endX, endY) = face_coordinates[2], face_coordinates[3]
            gray_face = gray_img[startY:endY, startX:endX]
            try:
                gray_face = cv2.resize(gray_face, self.__emotion_target_size)
            except Exception as e:
                print("{} resize failed".format(gray_face.shape))
                continue

            if not self.deployment:

                # Local Keras model
                gray_face = self.__preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = self.__emotion_classifier.predict(
                    gray_face)[0]
                labelled_emotions = {
                    self.__labels[idx]: round(score, 2)
                    for idx, score in enumerate(emotion_prediction)
                }
            elif self.deployment:
                emotion_prediction = self.__emotion_classifier.predict(
                    gray_face)
                labelled_emotions = {
                    emotion: round(score, 2)
                    for emotion, score in emotion_prediction.items()
                }
            else:
                raise NotImplemented()

            emotions.append({
                'coordinates': face_coordinates,
                'emotions': labelled_emotions
            })
        return emotions


def parse_arguments(args):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', type=str, help='Image filepath')
    return parser.parse_args()


def inference():
    args = parse_arguments(sys.argv)
    ed = Emotion_detector()
    inference = ed.detect_emotion(args.image)
    print(inference)


def main(args=None):
    pass


if __name__ == '__main__':
    main()
