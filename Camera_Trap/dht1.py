from simpleGPS import simpleGPS


obj= simpleGPS()

obj.power_on(7)
obj.send_at('AT+CGNSPWR=1,1','OK',1)
while True:
    answer = obj.send_at('AT+CGNSINF','+CGNSINF: ',1)
    
    if isinstance(answer, list):
        # Code to execute if 'data' is an array (list)
        print(answer[0])
        print(answer[1])
        print(answer[2])
        time.sleep(5)
        
    else:
        # Code to execute if 'data' is not an array
        print(answer)
