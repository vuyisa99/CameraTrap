import RPi.GPIO as GPIO
import time
import psutil
import subprocess

class BITE_data:
    def __init__(self):
        self.temperature = None
        self.POWER_SUPPLY_PIN = 16
    #-----------------------------------------------------POWER SUPPLY-------------------------------------------------------------------------
    # Set the GPIO pin connected to the power supply status
      # Replace with the actual GPIO pin number

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.POWER_SUPPLY_PIN, GPIO.IN)

    def is_power_supply_on(self):
        supply = GPIO.input(self.POWER_SUPPLY_PIN)
        return supply
    #----------------------------------------------------POWER SUPPLY ENDS--------------------------------------------------------------------------


    #----------------------------------------------------CPU TEMPERATURE----------------------------------------------------------------------------
    def get_cpu_temperature(self):
        try:
            # Run the command and capture its output
            result = subprocess.check_output(["/usr/bin/vcgencmd", "measure_temp"])

            # Decode the bytes to a string and extract the temperature value
            temperature_str = result.decode("utf-8").strip()
            self.temperature = float(temperature_str.split("=")[1].split("'")[0])

            return self.temperature
        except subprocess.CalledProcessError as e:
            # Handle any errors that may occur during command execution
            print(f"Error: {e}")
            return None
        except (ValueError, IndexError, KeyError):
            # Handle parsing errors
            print("Unable to retrieve CPU temperature.")
            return None
    #----------------------------------------------------CPU TEMP ENDS-------------------------------------------------------------------------------
# def main():
#     monitor = BITE_data()
#     monitor.__init__()
#     CPU_temp=monitor.get_cpu_temperature()
#     monitor.setup_gpio()
#     supply=monitor.is_power_supply_on()
#     print(CPU_temp,supply)
#     
# if __name__ == "__main__":
#     main()