
import RPi.GPIO as GPIO

class PIRsensor:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.PIRpin=18 #pin
        GPIO.setup(self.PIRpin,GPIO.IN)#sensor_type
        #, pin, sensor_type

    def monitor(self):
        motion=GPIO.input(self.PIRpin)
        return motion