#!/usr/bin/python
# Filename: text.py
import serial
import time
import RPi.GPIO as GPIO
import re
ser = serial.Serial("/dev/ttyS0",115200)

W_buff = ["AT+CGNSPWR=1\r\n", "AT+CGNSSEQ=\"RMC\"\r\n", "AT+CGNSINF\r\n", "AT+CGNSURC=2\r\n","AT+CGNSTST=1\r\n"]
ser.write(W_buff[0].encode())
ser.flushInput()
data = ""
num = 0

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7, GPIO.OUT)

try:
    #GPIO.output(7, GPIO.LOW)
    #time.sleep(4)
    #GPIO.output(7, GPIO.HIGH)
    #time.sleep(10)
    #GPIO.cleanup()
    while True:
        #print ser.inWaiting()
        print('not working')
        while ser.inWaiting() > 0:
            data += str(ser.read(ser.inWaiting()))
        if data != "":
            #print (data)
            if  num < 4: # the string have ok
                #print (num)
                time.sleep(0.5)
                ser.write(W_buff[num+1].encode())
                num =num +1
            if num == 4:
                time.sleep(0.5)
                ser.write(W_buff[4].encode())
                print(data)
            
            data = ""
            print('////////////////////////////////////////')
            time.sleep(10)
        time.sleep(1)
            
except KeyboardInterrupt:
    if ser != None:
        ser.close()
        
