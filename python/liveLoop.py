### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

#importing and setting up classes
import numpy as np
import time
import cv2 as cv
# import gpiod
# from smbus import SMBus
from theController import theControllerClass
from waterDetectorClass import waterDetector

# files
input_file = "angleTest.avi"
output_file = "angleTestOUT.mp4"
outputFlag = False
displayFlag = True

# controller setup
controller = theControllerClass()
start = time.time()
timeOld = time.time()

# water detector setup
wd = waterDetector()

# i2c set up
addr = 0x8 # bus address
# bus = SMBus(1) # indicates /dev/ic2-1

firstLoop = True
beginTime = time.time() # moved from inside loop

cap = cv.VideoCapture(0)

while True:
    if firstLoop: firstLoop = False
	
    #Time set ups
    timeNow = time.time()
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow
    
    ret, frame = cap.read()
    
    measAngle, frame, gray_blurred, frame_delta, mask = wd.loop(firstLoop,frame)

    refAngle = controller.ref(elapsedTime)

    ctrlAngle = controller.control(elapsedTime, refAngle, measAngle)

    print("MEASURED ANGLE: ",measAngle)
    print("REFERENCE ANGLE: ",refAngle)
    print("CONTROL ANGLE: ",ctrlAngle)

    cv.imshow("look! cool!", frame)
    ch = cv.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

# clean up
cv.waitKey(0)
cv.destroyAllWindows()
cap.release()














### RESOURCES AND DEPRECIATED CODE ###

#  https://dronebotworkshop.com
#  https://dronebotworkshop.com/i2c-arduino-raspberry-pi/
#  https://roboticsbackend.com/raspberry-pi-master-arduino-slave-i2c-communication-with-wiringpi/
  
  
# calFlagPin = 17  # GPIO 17, physical pin 11
# chip = gpiod.Chip('gpiochip4')
# calFlagLine = chip.get_line(calFlagPin)
# calFlagLine.request(consumer="Arduino", type=gpiod.LINE_REQ_DIR_OUT)
# calFlagLine.set_value(0)
  
    # #i2c modes
    # mode = input("What mode would you like to run?\n[cal] [step] [hold] [per] [abs]\n>>>>    ")
  
    # if mode == "cal":
    #     print("Entering calibration mode")
    #     calFlagLine.set_value(1)
    #     calLoop = True
    #     while calLoop:
    #         calIn = input("Enter relative angle or [exit]: ")
    #         if calIn == "exit": 
    #             calLoop == False
    #             break
    #         else: print(calIn)
	# 		# bus.write_byte(addr,int(calIn))
    #     print("Exitting calibration mode...")
    #     calFlagLine.set_value(0)

    # elif mode == "abs":
    #     print("Entering absolute position mode")
    #     absLoop = True
    #     while absLoop:
    #         absIn = input("Enter absolute angle in degrees or [exit]: ")
    #         if absIn == "exit": 
    #             absLoop = False
    #             break
    #         else: print(int(absIn))
	# #		bus.write_byte(addr,int(angle))
    #     print("Exitting absolute position mode...")

    # else:
    #     mode = input("invalid input/nWhat mode would you like to run?\n[cal] [step] [hold] [per] [abs]\n>>>>    ")
# calFlagLine.release()