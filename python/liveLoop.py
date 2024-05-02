### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

#importing and setting up classes
import time
import os
import numpy as np
import cv2 as cv
# import gpiod
# from smbus import SMBus
from theController import theControllerClass
from waterDetectorClass import waterDetector

# files
input_file = "angleTest.avi"
output_file = "angleTestIntegratedOUT.mp4"
filePath = os.path.realpath(__file__)
fileDir = os.path.dirname(filePath)
inDir = fileDir.replace('python', 'inputVids')
outDir = fileDir.replace('python', 'outputVids')
input_path = os.path.join(inDir,input_file)
output_path = os.path.join(outDir,output_file)

# i/o flags
inputFlag = True # True for webcam, False for input file
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

# instantiate capture object
if inputFlag: cap = cv.VideoCapture(0)
else: cap = cv.VideoCapture(input_path)
ret, test_frame = cap.read()
if not ret:
    print("Failed to get frame from camera.")
    cap.release()
    exit()

actual_frame_height, actual_frame_width = test_frame.shape[:2]
frame_height = actual_frame_height + 150  # Adding space for text
size = (actual_frame_width, actual_frame_height)

if outputFlag: result = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*"mp4v"), 30, size)

# pre-loop assignments
firstLoop = True
angle = 0
measAngleLast = 0

while True:
    if firstLoop: firstLoop = False
	
    #Time set ups
    timeNow = time.time()
    beginTime = time.time() # moved from inside loop
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow
    
    ret, frame = cap.read()
    

    measAngle, frame, gray_blurred, frame_delta, mask = wd.loop(firstLoop,frame)
    if measAngle == None: measAngle = measAngleLast
    measAngleLast = measAngle

    refAngle = controller.ref(elapsedTime)

    ctrlAngle = controller.control(elapsedTime, refAngle, measAngle)

    # print("MEASURED ANGLE: ",measAngle)
    # print("REFERENCE ANGLE: ",refAngle)
    # print("CONTROL ANGLE: ",ctrlAngle)
    # print("ELAPSED TIME: ", elapsedTime)

    # Prepare frame with text space
    frame_with_text = np.zeros((frame_height, actual_frame_width, 3), dtype=np.uint8)
    frame_with_text[:actual_frame_height, :, :] = frame  # Only copy the video part, ensure dimensions match

    # Generate info text
    if ctrlAngle == None: ctrlAngle = -1
    info_text = f"MEASURED ANGLE: {measAngle:.2f}\nREFERENCE ANGLE: {refAngle:.2f}\nCONTROL ANGLE: {ctrlAngle:.2f}\nELAPSED TIME: {int(time.time() - start)} sec"

    # Display text on frame
    y0, dy = actual_frame_height + 30, 30  # Start text 10 pixels below the original frame
    for i, line in enumerate(info_text.split('\n')):
        y = y0 + i * dy
        cv.putText(frame_with_text, line, (10, y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv.imshow("Output Frame", frame_with_text)

    if outputFlag: result.write(frame)

    ch = cv.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

# clean up
cv.waitKey(0)
cv.destroyAllWindows()
cap.release()
if outputFlag: result.release()
print("All done!")













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