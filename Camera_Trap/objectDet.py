#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import cv2
from picamera2 import Picamera2
import RPi.GPIO as GPIO
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
from backAgain import DHTSensor
from PIRsensor import PIRsensor
import time
from datetime import datetime, timedelta
import re
import math


model='efficientdet_lite0.tflite'
num_threads=4



picam2 = Picamera2()
dispW=640
dispH=360
picam2.preview_configuration.main.size = (dispW,dispH)
picam2.preview_configuration.main.format = "RGB888"
"picam2.preview_configuration.controls.FrameRate=30"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()


pos=(5,355)
font=cv2.FONT_HERSHEY_SIMPLEX
height=.3
weight=1
textColor=(255,255,255)
upperLeft = (0,340)
lowerRight = (639,359)
thickness = -1
boxColor = (0,0,0)
fps=0

base_options=core.BaseOptions(file_name=model,use_coral=False, num_threads=num_threads)
detection_options=processor.DetectionOptions(max_results=4,score_threshold=0.5)
options=vision.ObjectDetectorOptions(base_options=base_options,detection_options=detection_options)
detector=vision.ObjectDetector.create_from_options(options)


die=0
count=0
while True:
    PIR_sensor = PIRsensor()
    motion = PIR_sensor.monitor()
    time.sleep(1)
    print("No motion detected")    
    if motion==1:
        while True:
            img = picam2.capture_array() # capuring a frame from the camera
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # changing the frame to a frame that is compatble with TFlite
            imgTensor=vision.TensorImage.create_from_array(imgRGB) # final TFlite frame
            mydetections=detector.detect(imgTensor) # detecting objects
            # get category
#             category_name=''
#             for detect in mydetections.detections: 
#                 category_name=detect.categories[0].category_name
#                 if category_name =='person':
#                     print('a %s is detected',category_name)
#                 
            image=utils.visualize(img,mydetections) # adding the TF info to the original frame
            cv2.rectangle(img,upperLeft,lowerRight,boxColor,thickness)
            #count=count+1
            cv2.imshow("picam2", img) # showing the frame to the screen
            cv2.imwrite('/home/vuyisa/Documents/testing_cat/'+'img'+str(count)+'.jpg', img)
            count=count+1
            time.sleep(1)
            if cv2.waitKey(1)==ord('q'):    # exiting the camera while loop
                die = 1
    if die==1:
        break
        
GPIO.cleanup()
print('all good')
cv2.destroyAllWindows()


