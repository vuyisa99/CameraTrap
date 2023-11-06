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
import serial
import sqlite3
import random
from Infoquery import mylora
from SX127x.board_config import BOARD2 as BOARD


#----LORA---
BOARD.setup()
BOARD.reset()
#---LORA---

#--------------------------------BITE_CONNECT----------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(5)
#--------------------------------BITE_CONNECT ENDS-----------------------


#-------------------------------------CAMERA SETUP--------------------------------------------------
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
#-------------------------------------------------CAMERA ENDS---------------------------------

#-------------------------------------------------GPS-TIME--------------------------------------

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

power_key = 7
rec_buff = ''
rec_buff2 = ''
time_count = 0

def send_at(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if command=='AT+CGNSINF':
            global GPSDATA
            #print(GPSDATA)
            #GPSDATA = rec_buff.decode().split(',')
            try:
                GPSDATA = str(rec_buff.decode())
                GPSDATA = GPSDATA.split('\n')
                GPSDATA = GPSDATA[1].split(',')
                GPSDATA = GPSDATA[2:5]
                if GPSDATA[0] != '':
                    SAST = float(GPSDATA[0])
                    date_str = str(SAST)
                    date_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S.%f')
                    date_obj += timedelta(hours=2)
                    GPSDATA[0] = str(date_obj)
                    return GPSDATA
                else:
                    return 'GPS not ready'
                
            except UnicodeDecodeError:
                return 'Could not decode data'
            
            
    else:
        return 'GPS not ready out'
    
    

def power_on(power_key):
    print('SIM868 is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM868 is ready')
#-------------------------------------------------GPS-TIME ENDS-------------------------------
 
 
#-------------------------------------------------SQLDB--------------------------------------
# Connect to the database
# conn = sqlite3.connect('CameraTrapRecords.db')
# cursor = conn.cursor()

#-------------------------------------------------SQLDB ENDS--------------------------------


#-------------------------------------------------LORA----------------------------------------
# when want to use just dendent
lora = mylora(verbose=False)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

#     Slow+long range  Bw = 125 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_spreading_factor(12)
lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
lora.set_low_data_rate_optim(True)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)



assert(lora.get_agc_auto_on() == 1)

# try:
#     print("START")
#     lora.start()
# except KeyboardInterrupt:
#     sys.stdout.flush()
#     print("Exit")
#     sys.stderr.write("KeyboardInterrupt\n")
# finally:
#     sys.stdout.flush()
#     print("Exit")
#     lora.set_mode(MODE.SLEEP)
# BOARD.teardown()
#-------------------------------------------------LORA ENDS-----------------------------------
die=0  # used to exit the outer while loop below
count = 0
#power_on(power_key)
#send_at('AT+CGNSPWR=1,1','OK',1)
PIR_sensor = PIRsensor()
dht_sensor = DHTSensor()

while True:
    #PIR_sensor = PIRsensor()
    motion = PIR_sensor.monitor()
    time.sleep(3)
    print("Nothing yet...")
    clientsocket, address = s.accept()
    print('client')
    confirmation_message = clientsocket.recv(1024).decode('utf-8')
    if confirmation_message == "ConnectionConfirmed":
        humidity, temperature = dht_sensor.read_data()
        time = str(random.uniform(0, 23))
        latitude = str(random.uniform(-90.0, 90.0))
        list_array = [str(humidity),str(temperature),time,latitude]
        serialized_list = pickle.dumps(list_array)
        clientsocket.send(serialized_list)
        #time.sleep(3)
    else:
        pass
        
    #start LoRa
#     try:
#     print("START")
#     lora.start()
#     except KeyboardInterrupt:
#         sys.stdout.flush()
#         print("Exit")
#         sys.stderr.write("KeyboardInterrupt\n")
#     finally:
#         sys.stdout.flush()
#         print("Exit")
#         lora.set_mode(MODE.SLEEP)
    # finish LoRa
    
    if motion==1:
        while True:
#             GPS_time = send_at('AT+CGNSINF','+CGNSINF: ',1)
#             time.sleep(2)
            humidity, temperature = dht_sensor.read_data()
            #share_data.update_shared_data(humidity,temperature,motion,str(random.uniform(-90.0, 90.0)),str(random.uniform(-90.0, 90.0)))
            #data = share_data.get_shared_data()
            #print(data["temperature"])
            #print(data["humidity"])
#             print(GPS_time)
              # Insert data into the CameraTrapRecords table
#             cursor.execute('''
#                 INSERT INTO CameraTrapRecords (timestamp, temperature, humidity, latitude, longitude)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (timestamp, temperature, humidity, latitude, longitude))
#             conn.commit()
#             count +=count
#             if count==5:
#                 conn.close()
#                 die=1
#                 break
            img = picam2.capture_array() # capuring a frame from the camera
            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # changing the frame to a frame that is compatble with TFlite
            imgTensor=vision.TensorImage.create_from_array(imgRGB) # final TFlite frame
            mydetections=detector.detect(imgTensor) # detecting objects
            # get category
            category_name=''
            for detect in mydetections.detections: 
                category_name=detect.categories[0].category_name
                if category_name =='person':
                    print('a %s is detected',category_name)
                
            image=utils.visualize(img,mydetections) # adding the TF info to the original frame
            cv2.rectangle(img,upperLeft,lowerRight,boxColor,thickness)
             
#             if isinstance(GPS_time, list):
#                 cv2.putText(img,'SAST: %s' % GPS_time[0]+' '+f'Temperature: {temperature:.1f}°C'+' '+f'Humidity: {humidity:.1f}%'+'GPS: '+GPS_time[1]+' '+GPS_time[2] , pos,font,height,textColor,weight) #annotating the frame
#             #cv2.imwrite('/home/vuyisa/Documents/images/'+'img'+str(count)+'.jpg', img)
#             else:
#                 cv2.putText(img,'SAST: --' + ' '+f'Temperature: {temperature:.1f}°C'+' '+f'Humidity: {humidity:.1f}%'+' GPS: '+'--'+' '+'--' , pos,font,height,textColor,weight)
            count=count+1
            cv2.imshow("picam2", img) # showing the frame to the screen
            time.sleep(1)
            if cv2.waitKey(1)==ord('q'):    # exiting the camera while loop
                die = 1
                break

    #humidity, temperature = dht_sensor.read_data()
    #share_data.update_shared_data(humidity,temperature,motion,str(random.uniform(-90.0, 90.0)),str(random.uniform(-90.0, 90.0)))
    if die==1:
        break
        
GPIO.cleanup()
print('all good')
cv2.destroyAllWindows()
#BOARD.teardown()

