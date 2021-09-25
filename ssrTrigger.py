from gpiozero import LED
import time

def trigerForTime(period):
   ssr=LED(18)
   ssr.on()
   time.sleep(period)
   ssr.off()
   return()
   