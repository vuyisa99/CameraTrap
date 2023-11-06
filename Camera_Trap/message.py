#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

import serial
import time
import math
import re


ser = serial.Serial('/dev/ttyS0',115200)
ser.flushInput()

phone_number = '0626200535'
text_message = 'person detected'

power_key = 7
rec_buff = ''
rec_buff2 = ''
time_count = 0


class message:
    def __init__(self):
        ser = serial.Serial('/dev/ttyS0',115200)
        ser.flushInput()

        self.phone_number = '0626200535'
        self.text_message = 'person detected'

        rec_buff = ''
        rec_buff2 = ''
    def SendShortMessage(self):#(phone_number,text_message):
        self.send_at2("AT+CMGF=1","OK",1)
        answer = self.send_at2("AT+CMGS=\""+self.phone_number+"\"",">",2)
        if 1 == answer:
            ser.write(self.text_message.encode())
            ser.write(b'\x1A')
            answer = self.send_at3('','OK',20)
            if 1 == answer:
                print('send successfully')
            else:
                print('error')
        else:
            print('error%d'%answer)
        #power_down(power_key)

    def send_at2(self,command,back,timeout):
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

    def send_at3(self,command,back,timeout):
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
        
    def ALERT(self):
        self.__init__()
        self.SendShortMessage()



    



