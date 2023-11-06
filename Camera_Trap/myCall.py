#!/usr/bin/python
# Filename: text.py
import serial
import time

#print('hello world0.')
ser = serial.Serial("/dev/ttyS0",115200)

W_buf_logoin = b"AT+CREG?\r\n"
W_buf_phone =  "ATD0626200535;\r\n".encode()
ser.write(W_buf_logoin)

#print W_buf_logoin

ser.flushInput()
data = ""
#print('hello world.')

try:
    print('hello world2.')
    while True:
        print('inside the loop.')
        time.sleep(1)
        while ser.inWaiting() > 0:
            print('first the loop')
            data += str(ser.read(ser.inWaiting()))
            time.sleep(0.0001)
        if data != "":
            print (data)
            if "CREG" in data:
                print ("call phone")
                ser.write(W_buf_phone)
            data = ""
    print('hello world3.')
except KeyboardInterrupt:
    if ser != None:
        ser.close()