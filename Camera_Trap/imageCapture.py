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

die=0
count=0
PIR_sensor = PIRsensor()
while True:
    while not PIR_sensor.monitor():
        pass
    Tstart = time.time()
    img = picam2.capture_array() # capuring a frame from the camera
    trigger_speed = time.time() - Tstart
    print(PIR_sensor.monitor())
    print(trigger_speed)
    cv2.imwrite('/home/vuyisa/Documents/image_Capture/'+'img'+str(count)+'.jpg', img)
    count=count+1
#     motion = PIR_sensor.monitor()
#     print("No motion detected")    
#     if motion==1:
#         print('motion detected')
#         Tstart = time.time()
#         while :
#             img = picam2.capture_array() # capuring a frame from the camera
#             #cv2.imshow("picam2", img) # showing the frame to the screen
#             cv2.imwrite('/home/vuyisa/Documents/image_Capture/'+'img'+str(count)+'.jpg', img)
#             
#             count=count+1
#             time.sleep(1)
#             if cv2.waitKey(1)==ord('q'):    # exiting the camera while loop
#                 die = 1
#     if die==1:
#         break
        
GPIO.cleanup()
print('all good')
cv2.destroyAllWindows()



