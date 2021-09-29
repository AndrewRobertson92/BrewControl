'''quick and dirty temp controler'''

from gpiozero import LED
import time
import os
import glob

def trigerForTime(period):
   ssr=LED(18)
   ssr.on()
   time.sleep(period)
   ssr.off()
   return()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def readTempC():
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

timeElapsed=0
mashTime=90*60
mashTarget = 68
while timeElapsed <= mashTime:
    curentTemp=readTempC()
    if curentTemp <= mashTarget:
       trigerForTime(2)
    else:
        time.sleep(2)
    timeElapsed += 2