
import Adafruit_DHT

class DHTSensor:
    def __init__(self):
        self.pin = 21 #pin
        self.sensor_type = Adafruit_DHT.DHT11#sensor_type
        #, pin, sensor_type

    def read_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_type, self.pin)
        return humidity, temperature

# if __name__ == "__main__":
#     # Set the GPIO pin you've connected the DHT11 sensor to
#     #DHT_PIN = 21  # Change this to the actual GPIO pin number
# 
#     # Specify the DHT sensor type (DHT11 or DHT22)
#     #DHT_TYPE = Adafruit_DHT.DHT11
# 
#     dht_sensor = DHTSensor()#DHT_PIN, DHT_TYPE)
# 
#     try:
#         humidity, temperature = dht_sensor.read_data()
# #         while True:
# #             humidity, temperature = dht_sensor.read_data()
# # 
# #             if humidity is not None and temperature is not None:
# #                 print(f'Temperature: {temperature:.1f}°C')
# #                 print(f'Humidity: {humidity:.1f}%')
# #             else:
# #                 print('Failed to retrieve data from the sensor.')
# 
#     except KeyboardInterrupt:
#         print('Measurement stopped by the user.')
# 
#     except Exception as e:
#         print(f'Error: {str(e)}')
