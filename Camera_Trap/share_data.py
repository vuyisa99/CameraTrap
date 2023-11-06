import sys
sys.path.append("/home/vuyisa/pySX1278")

# class share_data:
    
    
# Define shared variables or data structures
humidity = 0
temperature =0
motion = 0
timestamp = ''
latitude = ''
longitude=''

# Function to update shared data
def update_shared_data(hum,temp,mot,time,lat):
    global humidity
    global temperature
    global motion
    global timestamp
    global latitude
    humidity = hum
    temperature=temp
    motion=mot
    timestamp = time
    latitude = lat
    
# Function to retrieve shared data
def get_shared_data():
    my_dict = {
    "humidity": humidity,
    "temperature": temperature,
    "motion": motion,
    "timestamp": timestamp,
    "latitude": latitude
    }
    return my_dict
