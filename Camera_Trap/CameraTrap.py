#!/usr/bin/python
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
import sys
sys.path.append("/home/vuyisa/pySX1278")
from LORA_CLIENT import mylora
sys.path.append("/home/vuyisa/pySX1278/SX127x")
from SX127x.board_config import BOARD2 as BOARD
from SX127x.LoRa import *
from BITE_data import BITE_data
import random
from message import message



#----LORA---
BOARD.setup()
BOARD.reset()
#---LORA---

#-------------------------------------SQL DB------------------------------------
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertCameraTrapRecord(timestamp, temperature, humidity, latitude, longitude, category_name, image_file):
    try:
        sqliteConnection = sqlite3.connect('CameraTrapRecords.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """INSERT INTO CameraTrapRecords
                                      (timestamp, temperature, humidity, latitude, longitude, category_name, image)
                                      VALUES (?, ?, ?, ?, ?, ?, ?)"""

        image_data = convertToBinaryData(image_file)
        data_tuple = (timestamp, temperature, humidity, latitude, longitude, category_name, image_data)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        #print("Camera trap record inserted successfully into the table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert camera trap record into SQLite table:", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection is closed")

#-------------------------------------SQL DB ENDS--------------------------------
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
phone_number = '0626200535'
text_message = ''


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
                if len(GPSDATA)>0 and GPSDATA[0] != '':
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
 

# #-------------------------------------------------LORA----------------------------------------
class mylora(LoRa2):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        BOARD.led_on()
        #print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True )# Receive INF
        print ("Receive: ")
        mens=bytes(payload).decode("utf-8",'ignore')
        mens=mens[2:-1] #to discard \x00\x00 and \x00 at the end
        print('('+mens+')')
        BOARD.led_off()
        if mens=='BITE':
            try:
             img = picam2.capture_array()
             image = 1
            except:
                image = 0
            dht_sensor = DHTSensor()
            GPS_time = send_at('AT+CGNSINF','+CGNSINF: ',1)
            humidity, temperature = dht_sensor.read_data()
            monitor = BITE_data()
            monitor.__init__()
            CPU_temp=monitor.get_cpu_temperature()
            monitor.setup_gpio()
            supply=monitor.is_power_supply_on()
            print("Equipment status required")
            msg =  f"{humidity},{temperature},{CPU_temp},{supply},{GPS_time[0]},{GPS_time[1]},{image}" 
            time.sleep(1)
#             print ("Send mens: DATA RASPBERRY PI")
            bytes_msg = msg.encode('ascii')
            payload_list =  [255, 255, 0, 0] + list(bytes_msg) + [0]
            self.write_payload(payload_list)
            self.set_mode(MODE.TX)
        else:
            #print('database')
            try:
                conn = sqlite3.connect('CameraTrapRecords.db')
                cursor = conn.cursor()
                if '*' in mens:
                     mens = mens.replace('*', 'id, timestamp, temperature, humidity, latitude, longitude, category_name')
                cursor.execute(mens)
                data = cursor.fetchall()
                count = 0
                string_data = [','.join(map(str, item)) for item in data]
                for row in string_data:
                    time.sleep(5)
                    #print ('here is row: ',row)
                    bytes_msg = row.encode('ascii')
                    payload_list =  [255, 255, 0, 0] + list(bytes_msg) + [0]
                    self.write_payload(payload_list)
                    self.set_mode(MODE.TX)
                    count+=1
                    print(count)
                    if count == 10:
                        break
            except sqlite3.Error as e:
                row = 'something went wrong'
                bytes_msg = row.encode('ascii')
                payload_list =  [255, 255, 0, 0] + list(bytes_msg) + [0]
                self.write_payload(payload_list)
                self.set_mode(MODE.TX)
        #conn.commit()
        print('outside...')
        time.sleep(3)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        die=0  # used to exit the outer while loop below
        count = 0
        #power_on(power_key)
        send_at('AT+CGNSPWR=1,1','OK',1)
        PIR_sensor = PIRsensor()
        dht_sensor = DHTSensor()
        while True:
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            while True:
                motion = PIR_sensor.monitor()
                time.sleep(1)
                print("Nothing yet...")
                num =  0
                if motion==1:
                    delay =time.time()
                    while (time.time() - delay < 10):
                        GPS_time = send_at('AT+CGNSINF','+CGNSINF: ',1)
                        humidity, temperature = dht_sensor.read_data()
                        img = picam2.capture_array() # capuring a frame from the camera
                        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # changing the frame to a frame that is compatble with TFlite
                        imgTensor=vision.TensorImage.create_from_array(imgRGB) # final TFlite frame
                        mydetections=detector.detect(imgTensor) # detecting objects
                        # get category
                        category_name=''
                        for detect in mydetections.detections: 
                            category_name=detect.categories[0].category_name
                            if category_name =='person':
                                print(category_name)
                                text_message = 'person detected'
                                if num==0:
                                    obj = message()
                                    obj.ALERT()
                                    num = num+1
                        #image=utils.visualize(img,mydetections) # adding the TF info to the original frame
                        cv2.rectangle(img,upperLeft,lowerRight,boxColor,thickness)
                         
                        if isinstance(GPS_time, list):
                            cv2.putText(img,'SAST: %s' % GPS_time[0]+' '+f'Temperature: {temperature:.1f} C'+' '+f'Humidity: {humidity:.1f}% '+'GPS: '+GPS_time[1]+' '+GPS_time[2]+f' Category: {category_name}' , pos,font,height,textColor,weight) #annotating the frame

                        else:
                            cv2.putText(img,'SAST: --' + ' '+f'Temperature: {temperature:.1f}°C'+' '+f'Humidity: {humidity:.1f}%'+' GPS: '+'--'+' '+'--' +f'Category: {category_name}' , pos,font,height,textColor,weight)
                        
                        # Insert data into the CameraTrapRecords table

                        #cv2.imshow("picam2", img) # showing the frame to the screen
                        cv2.imwrite('/home/vuyisa/Documents/images/'+'img'+str(count)+'.jpg', img)
                        time.sleep(1)
                        image_file = '/home/vuyisa/Documents/images/'+'img'+str(count)+'.jpg'
                        count=count+1
                        insertCameraTrapRecord(GPS_time[0], temperature, humidity, GPS_time[1], GPS_time[2], category_name, image_file)
                        time.sleep(3)
                        if cv2.waitKey(1)==ord('q'):    # exiting the camera while loop
                            die = 1
                            break
                if die==1:
                    break
            if die ==1:
                break

lora = mylora(verbose=False)
#args = parser.parse_args(lora) # configs in LoRaArgumentParser.py

#     Slow+long range  Bw = 250 kHz, Cr = 4/8, Sf = 4096chips/symbol, CRC on. 13 dBm
lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_bw(BW.BW250)
lora.set_coding_rate(CODING_RATE.CR4_8)
lora.set_spreading_factor(12)
lora.set_rx_crc(True)
#lora.set_lna_gain(GAIN.G1)
#lora.set_implicit_header_mode(False)
lora.set_low_data_rate_optim(True)

#  Medium Range  Defaults after init are 434.0MHz, Bw = 125 kHz, Cr = 4/5, Sf = 128chips/symbol, CRC on 13 dBm
#lora.set_pa_config(pa_select=1)



try:
    assert(lora.get_agc_auto_on() == 1)
except Exception as e:
    GPIO.cleanup()
    print('get outo on failed: ',e)
    BOARD.teardown()
    print('teardown complete...')


#-------------------------------------------------LORA ENDS-----------------------------------


try:
    print("START")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
    if ser != None:
        ser.close()
    GPIO.cleanup()
    BOARD.teardown()
finally:
    sys.stdout.flush()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
GPIO.cleanup()
print('all good')
cv2.destroyAllWindows()
BOARD.teardown()



