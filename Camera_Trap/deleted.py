#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO

import serial
import time

ser = serial.Serial('/dev/ttyS0',115200)
ser.write("AT+CGNSPWR=1\r\n".encode())
ser.flushInput()

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
		if back not in rec_buff.decode():
			print(command + ' ERROR')
			print(command + ' back:\t' + rec_buff.decode())
			return 0
		else:
			
			#print(rec_buff.decode())
			
			#Additions to Demo Code Written by Tim!
			global GPSDATA
			#print(GPSDATA)
			GPSDATA = str(rec_buff.decode())
			Cleaned = GPSDATA[16:]
			
			#print(Cleaned)
			
			Lat = Cleaned[:2]
			SmallLat = Cleaned[2:11]
			NorthOrSouth = Cleaned[12]
			
			print('Lat: '+ Lat,' smallLat: '+ SmallLat,' NorthOrSouth: '+ NorthOrSouth)
# 			
# 			Long = Cleaned[14:17]
# 			SmallLong = Cleaned[17:26]
# 			EastOrWest = Cleaned[27]
# 			
# 			#print(Long, SmallLong, EastOrWest)   
# 			FinalLat = float(Lat) + (float(SmallLat)/60)
# 			FinalLong = float(Long) + (float(SmallLong)/60)
# 			
# 			if NorthOrSouth == 'S': FinalLat = -FinalLat
# 			if EastOrWest == 'W': FinalLong = -FinalLong
# 			
# 			print(FinalLat, FinalLong)
# 			
# 			#print(FinalLat, FinalLong)
# 			#print(rec_buff.decode())
			
			return 1
	else:
		print('GPS is not ready')
		return 0

def get_gps_position():
	rec_null = True
	answer = 0
	print('Start GPS session...')
	rec_buff = ''
	send_at('AT+CGNSPWR=1,1','OK',1)
	time.sleep(2)
	while rec_null:
		answer = send_at('AT+CGNSINF','+CGNSINF: ',1)
		if 1 == answer:
			answer = 0
			if ',,,,,,' in rec_buff:
				print('GPS is not ready')
				rec_null = False
				time.sleep(1)
		else:
			print('error %d'%answer)
			rec_buff = ''
			send_at('AT+CGNSPWR=0','OK',1)
			return False
		time.sleep(1.5)


while True:
	
	get_gps_position()
