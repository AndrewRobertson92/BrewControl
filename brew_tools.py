
#from gpiozero import LED
#from w1thermsensor import W1ThermSensor
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

def read_temp_c():


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



    

def PID_tune(integral_period):
    '''
    #roughly Ziegler–Nichols tunning method
    Sample rate is likely not high enough and does not have the temporal
    accuracy required to find stable oscilation conditions. additionally this
    is likely overkill for a process as simple and predictable as heating a pot
    of water so instead I will increase the proportionallity constant instill a
    signifcat overshoot is detected
    
    '''
    
    target_temp=65
    k_p=15*4.12/2.5 #starting proportional constant 
    while True:
        
        process_value=read_temp_c()
        print(process_value)
        error_value=(target_temp-process_value)
        #print(error_value)
        duty_cycle=k_p*error_value
        #print(duty_cycle)
        if duty_cycle <= 0:
            duty_cycle = 0.0
        #if duty_cycle >= 1:
            #duty_cycle = 1
        
        #print(duty_cycle)
        on_time=duty_cycle*integral_period
        #print(on_time)
        triger_for_time(on_time)
        
        if on_time <= integral_period:
            
            time.sleep(integral_period-on_time)
                       
        process_value=read_temp_c()
         # cheack for significant overshot
        if process_value - target_temp >= 0:
            print(process_value)
            break
        
        #increase power by 10%
        k_p=k_p*1.1
    ultimate_gain= k_p
    return(ultimate_gain*0.5)
    
            
       
        
        # is the error va
        
        #if oscilation break
    

PID_tune(10)
