
from gpiozero import LED
from w1thermsensor import W1ThermSensor
import time
import os
import glob

simulated_pot_temp=20.0 #single variable for testing

''' turns process on for period seconds'''
def triger_for_time(period):
    
   ssr=LED(18)
   ssr.on()
   time.sleep(period)
   ssr.off()
   
   return()



def temp_read(method = "open_string"):
        
    ''' get's temperature from one wire sensor'''   
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    
    def read_temp_raw():
        while True:
            # The sensor is sometimes unresponsive generally sub 1s response time
            try:
                f = open(device_file, 'r')
                lines = f.readlines()
                f.close()
                break
            except:
                pass
        return lines
    
    def read_temp_open_string():   
    
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = int(temp_string) / 1000.0 # TEMP_STRING IS THE SENSOR OUTPUT, MAKE SURE IT'S AN INTEGER TO DO THE MATH
            temp_c = round(temp_c, 1) # ROUND THE RESULT TO 1 PLACE AFTER THE DECIMAL, THEN CONVERT IT TO A STRING
    
        return temp_c
    
    def read_temp_W1():
        from w1thermsensor import W1ThermSensor
        while True:
            try:
                sensor = W1THermSensor()
                temp_c = sensor.get_temperature()
                break
            except:
                pass
        return temp_c
    
    if method == "open_string":
        return read_temp_open_string()
    
    else if method == "w1_lib":
        read_temp_W1()
        


def proportional_control(k_p,target_temp,integral_period):
    process_value=read_temp_c("w1_lib")
    while process_value <= target_temp:
                                  
        process_value=read_temp_c("w1_lib")
        error_value=(target_temp-process_value)
        duty_cycle=k_p*error_value
        
        print(process_value)            
        if duty_cycle <= 0:
            duty_cycle = 0.0
        '''
        this shoudlnt be neceseery for a reasonably chosen 
        starting constant but just incase and to avoid filling 
        the brew hall with steam this caps the on time at a minuet
        '''
        if duty_cycle >= 6:
            duty_cycle = 6
                    
        on_time=duty_cycle*integral_period
        
        triger_for_time(on_time)
        
    
def PID_tune(final_taget_temp = 65,integral_period = 10,volume_of_water = 15):
    '''
    #roughly Ziegler–Nichols tunning method
    Sample rate is likely not high enough and does not have the temporal
    accuracy required to find stable oscilation conditions. additionally this
    is likely overkill for a process as simple and predictable as heating a pot
    of water so instead I will increase the proportionallity constant instill a
    signifcat overshoot is detected
    
    '''
    target_temp=final_target_temp-40 #in order to run concurent cycles without having to wait for the pot to call down
    k_p=volume_of_water*4.12/2.5 #starting proportional  volume*specific heat capacity/power = temprise per second  
    
    while True:
        # run proportional control untill target is reached
        proportional_control(k_p,target_temp,10)
        
        # evaluate overshoot
        process_value=read_temp_c("w1_lib")
        if process_value - target_temp >= 0.2: # this a reasonable overshoot for 10s integral time about half the theoretical maximum overshoot
            print(process_value)
            break
        
        #increase target value by 5 degrees c (cheack it's still reasonable)
        if target_temp <= 80:
            target_temp +=5
        else:
            Print("wait for pot to cool and restart tune with the returned value")
            break
        
        #increase power by 10%
        k_p=k_p*1.1
    ultimate_gain= k_p
    return(ultimate_gain*0.5)
    
            
       
        
  
    


