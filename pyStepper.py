import RPi.GPIO as GPIO
import time
import sys


GPIO.setmode(GPIO.BOARD)

DIR=33
PUL=35
ENA = 37

Sets=(DIR,PUL,ENA)

DIR_Left=GPIO.HIGH
DIR_Right=GPIO.LOW

ENA_Locked = GPIO.LOW
ENA_Released =GPIO.HIGH

GPIO.setwarnings(False)

GPIO.setup(Sets,GPIO.OUT)

steps=int(sys.argv[1])
direction = steps

GPIO.output(ENA, ENA_Locked)

if (steps<0):
   GPIO.output(DIR,DIR_Right)
else:
    GPIO.output(DIR,DIR_Left)

try:

 while(True):
  if (steps<0):
   GPIO.output(DIR,DIR_Right)
  else:
    GPIO.output(DIR,DIR_Left)

  for i in range(abs(steps)):
    GPIO.output(PUL,GPIO.HIGH)
    time.sleep(0.0001875)

    GPIO.output(PUL,GPIO.LOW)
    time.sleep(0.0001875)
 
  time.sleep(1)
 
  if (steps>0):
   steps=~steps+1
  else:
   steps=~steps-1

except KeyboardInterrupt:
    
  GPIO.output(ENA,ENA_Released)
  print("The motor has been stopped")

