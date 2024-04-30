### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

#importing and setting up classes
import numpy as np
import time
import gpiod
from smbus import SMBus
from theController import theControllerClass

controller = theControllerClass()
start = time.time()
timeOld = time.time()

#i2c set up
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

calFlagPin = 17  # GPIO 17, physical pin 11
chip = gpiod.Chip('gpiochip4')
calFlagLine = chip.get_line(calFlagPin)
calFlagLine.request(consumer="Arduino", type=gpiod.LINE_REQ_DIR_OUT)
calFlagLine.set_value(0)

calibrate = False
firstloop = True

while True:
	
    #Time set ups
    timeNow = time.time()
    beginTime = time.time()
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow

    #i2c modes
    mode = input("What mode would you like to run?\n[cal] [step] [hold] [per] [abs]\n>>>>    ")
	
    if mode == "cal":
        print("Entering calibration mode")
        calFlagLine.set_value(1)
        calLoop = True
        while calLoop:
            calIn = input("Enter relative angle or [exit]: ")
            if calIn == "exit": 
                calLoop == False
                break
            else: print(calIn)
			# bus.write_byte(addr,int(calIn))
        print("Exitting calibration mode...")
        calFlagLine.set_value(0)

    elif mode == "abs":
        print("Entering absolute position mode")
        absLoop = True
        while absLoop:
            absIn = input("Enter absolute angle in degrees or [exit]: ")
            if absIn == "exit": 
                absLoop = False
                break
            else: print(int(absIn))
	#		bus.write_byte(addr,int(angle))
        print("Exitting absolute position mode...")

    else:
        mode = input("invalid input/nWhat mode would you like to run?\n[cal] [step] [hold] [per] [abs]\n>>>>    ")
    
    
    controller.control()
    controller.ref()

    if firstLoop: firstLoop = False


calFlagLine.release()

#  https://dronebotworkshop.com
#  https://dronebotworkshop.com/i2c-arduino-raspberry-pi/
#  https://roboticsbackend.com/raspberry-pi-master-arduino-slave-i2c-communication-with-wiringpi/