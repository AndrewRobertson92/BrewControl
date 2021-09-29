from tempRead import readTempC
from ssrTrigger import trigerForTime
import time
from threading import Thread





class MashCycle:
    #mash class have properties
    def __init__(self,mashTime,targetTemp,p,d,intTime):
        self.mashTime = mashTime
        self.targetTemp = targetTemp
        self.p = p
        self.d = d
        self.cycleTime=intTime

    def warmUP(self):
        

        currentTemp=readTempC()
        #warm up phase
        while currentTemp <= (self.targetTemp-2):
            dutyCycle=1
            '''
            probably dont need to have proportional control on the warm up phase
            unless volume is verry low
            dutyCycle=self.p*((self.targetTemp-currentTemp+3)/currentTemp)
            if dutyCycle >= 1:
                dutyCycle = 1
            if dutyCycle <= 0:
                dutyCycle = 0
            '''
            trigerForTime(dutyCycle*self.intTime)
            time.sleep(self.intTime*(1-dutyCycle))
            currentTemp = readTempC()
            print(currentTemp)
        return()

    def mash(self):
        timeRunning=0
        currentTemp=readTempC()
        previousTemp=currentTemp
        while timeRunning <= self.mashTime :
            currentTemp = readTempC()
            dutyCycle=self.p*((self.targetTemp-currentTemp+3)/currentTemp) + self.d*(currentTemp-previousTemp)/self.cycleTime
            if dutyCycle >= 1:
                dutyCycle = 1
            if dutyCycle <= 0:
                dutyCycle = 0
            trigerForTime(dutyCycle*self.intTime)
            time.sleep(self.intTime*(1-dutyCycle))
            timeRunning+= self.intTime
            previousTemp=currentTemp
            currentTemp = readTempC()
            print(currentTemp)
        return

mashLength=90*60 #time in seconds
mashTemp=68
ToMash=MashCycle(90,25, 1, 0.001,10)

ToMash.warmUP()
print("ready")
ToMash.mash()



        
        



        



        



