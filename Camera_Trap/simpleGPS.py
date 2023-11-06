#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

import serial
import time
import math
import re
from datetime import datetime, timedelta
from backAgain import DHTSensor
from message import message

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
dht_sensor = DHTSensor()

ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

phone_number = '0626200535'
text_message = 'person detected'

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
                if isinstance(GPSDATA, list):
                    if len(GPSDATA) > 0 and GPSDATA[0] != '':
                        #print(f'start:{GPSDATA[0]}:end')
                        SAST = GPSDATA[0] #+ 20000.00
                        date_str = str(SAST)
                        date_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S.%f')
                        date_obj += timedelta(hours=2)
                        GPSDATA[0] = str(date_obj)#str(SAST)
                        return GPSDATA
                    else:
                        return 'GPS not ready'
                
            except UnicodeDecodeError:
                return 'Could not decode data'
            
            #print(GPSDATA)
            
    else:
        return 'GPS not ready out'
    
def SendShortMessage(phone_number,text_message):
    send_at2("AT+CMGF=1","OK",1)
    answer = send_at2("AT+CMGS=\""+phone_number+"\"",">",2)
    if 1 == answer:
        ser.write(text_message.encode())
        ser.write(b'\x1A')
        answer = send_at3('','OK',20)
        if 1 == answer:
            print('send successfully')
        else:
            print('error')
    else:
        print('error%d'%answer)
    #power_down(power_key)

def send_at2(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
        print(rec_buff)
    if back not in rec_buff.decode():
        print(command + ' ERROR')
        print(command + ' back:\t' + rec_buff.decode())
        return 0
    else:
        #print(rec_buff.decode())
        return 1

def send_at3(command,back,timeout):
    rec_buff = ''
    ser.write((command+'\r\n').encode())
    time.sleep(timeout)
    if ser.inWaiting():
        time.sleep(0.01 )
        rec_buff = ser.read(ser.inWaiting())
    if rec_buff != '':
        if back not in rec_buff.decode():
            print(command + ' ERROR')
            print(command + ' back:\t' + rec_buff.decode())
            return 0
        else:
            return 1
    else:
        return 0



    

def power_on(power_key):
    print('SIM7600X is starting:')
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(power_key,GPIO.OUT)
    time.sleep(0.1)
    GPIO.output(power_key,GPIO.HIGH)
    time.sleep(2)
    GPIO.output(power_key,GPIO.LOW)
    time.sleep(20)
    ser.flushInput()
    print('SIM7600X is ready')

#     def power_down(power_key):
#         print('SIM7600X is loging off:')
#         GPIO.output(power_key,GPIO.HIGH)
#         time.sleep(3)
#         GPIO.output(power_key,GPIO.LOW)
#         time.sleep(18)
#         print('Good bye')

#Additions to Demo GPS.py Code Added by Tim // Simplfing the GPS Start up process
#power_on(power_key)
#         
send_at('AT+CGNSPWR=1,1','OK',1)
count=0
while True:
    answer = send_at('AT+CGNSINF','+CGNSINF: ',1)
    
    if isinstance(answer, list):
        # Code to execute if 'data' is an array (list)
        #humidity, temperature = dht_sensor.read_data()
        print("date&time: ",answer[0])
        print('Latitude: ',answer[1])
        print('longitude: ',answer[2])
        count +=1
        if count == 6:
            #obj = message()
            #obj.ALERT()
            #SendShortMessage(phone_number,text_message)
            pass
        #print(humidity,temperature)
        #time.sleep(1)
        
    else:
        # Code to execute if 'data' is not an array
        print(answer)
    