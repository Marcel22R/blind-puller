import RPi.GPIO as GPIO
import time
import sys
import json
import argparse
from argparse import ArgumentParser
import os


steps_all_the_way=8000
stateFilePath="blindState.json"

def main():
    global stateFilePath
    parser=ArgumentParser()
    parser.add_argument("-p",type=dir_path,help="Path to the state file.")
    args=parser.parse_args()
    
    if os.path.exists(stateFilePath):
        move_blinds()
    else:
        new_path=os.path.join(args.p,stateFilePath)
        stateFilePath=new_path
        if(os.path.exists(stateFilePath)):
            move_blinds()



def move_blinds():
    state=checkState()
    if(state=="down"):
        blinds_up()
        switchBlindState()
    else:
        blinds_down()
        switchBlindState()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable dir: {path} is not a valid path")   

def switchBlindState():
    data=""
    with open(stateFilePath, "r") as f:
        data=json.load(f)

    print(data["blindState"]["position"])
    if(data["blindState"]["position"]=="down"):
        print("Switching state to up")
        data["blindState"]["position"]="up"
    else:
        print("Switching state to down")
        data["blindState"]["position"]="down"
    
    with open(stateFilePath,"w") as f:
        json.dump(data, f)

def checkState():
    with open(stateFilePath) as f:
        data=json.load(f)
        return data["blindState"]["position"]

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
