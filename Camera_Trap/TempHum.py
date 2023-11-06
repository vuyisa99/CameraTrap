
import RPi.GPIO as GPIO
#import dht1
import time
from backAgain import DHTSensor

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.cleanup()
print('TEMPERATURE IS RUNNING.....')

# read data using Pin GPIO21 
#instance = dht1.DHT11(pin=21)

try:
    #dht_sensor = DHTSensor()
    while True:
        dht_sensor = DHTSensor()
        #print('stuck')
        humidity, temperature = dht_sensor.read_data()
        if humidity is not None and temperature is not None:
            print(f'Temperature: {temperature:.1f}°C')
            print(f'Humidity: {humidity:.1f}%')

        time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
