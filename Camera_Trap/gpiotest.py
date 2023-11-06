import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Choose the GPIO pin number (replace with the desired pin number)
output_pin = 19

# Set the pin as an output
GPIO.setup(output_pin, GPIO.OUT)
GPIO.output(output_pin, GPIO.HIGH)
time.sleep(10)
GPIO.cleanup()
