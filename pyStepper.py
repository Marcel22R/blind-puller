import RPi.GPIO as GPIO
import time
import sys


steps_all_the_way=7000

def main():
    blinds_up()
    blinds_down()


def blinds_up():
    turn_x_steps(steps_all_the_way)    


def blinds_down():
    turn_x_steps(other_direction(steps_all_the_way))


def other_direction(number):
    return -1*number



#Positive values pull blinds up, negative let it back down
def turn_x_steps(steps):

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

    direction = steps

    GPIO.output(ENA, ENA_Locked)

    if (steps<0):
       GPIO.output(DIR,DIR_Right)
    else:
        GPIO.output(DIR,DIR_Left)

    try:

        for i in range(abs(steps)):
            GPIO.output(PUL,GPIO.HIGH)
            time.sleep(0.0001875)

            GPIO.output(PUL,GPIO.LOW)
            time.sleep(0.0001875)

        time.sleep(1)


    except KeyboardInterrupt:
        
      GPIO.output(ENA,ENA_Released)
      print("The motor has been stopped")






if __name__=="__main__":
    main()
