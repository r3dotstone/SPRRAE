### INPUT: position of stream from vision
### OUTPUT: demand for position to i2c

#importing and setting up classes
import time
import os
import imutils
import numpy as np
import cv2 as cv
# import gpiod
from smbus import SMBus
from angleXform import AngleXform
from theController import theControllerClass
from waterDetectorClass import waterDetector

# files
input_file = "angleTest.avi"
output_file = "test.mp4"
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


# environment setup
fieldStart = (380,300)
horzEnd = (94,194)
vertEnd = (381,130)

# water detector setup
wd = waterDetector()

# i2c set up
addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

# calibration logic
calInput = input("Enter a Calibration Angle or [start]: ")
calFlag = True
while calFlag == True:
    if calInput=="start": calFlag = False
    else: bus.write_byte(addr,int(calInput))
    if calFlag == True: calInput = input("Enter a Calibration Angle or [start]: ")

# instantiate capture object
if inputFlag: cap = cv.VideoCapture(0)
else: cap = cv.VideoCapture(input_path)
ret, test_frame = cap.read()

if not ret:
    print("Failed to get frame from camera.")
    cap.release()
    exit()

# sort out frame size for text and write out
adjustedWidth = 400
test_frame = imutils.resize(test_frame, width = adjustedWidth)

actual_frame_height, actual_frame_width = test_frame.shape[:2]
frame_height = actual_frame_height + 150  # Adding space for text
size = (actual_frame_width, frame_height)
# print(size)

if outputFlag: result = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*"mp4v"), 30, size)

# pre-loop assignments
firstLoop = True
angle = 0
measAngleLast = 0

# controller setup
controller = theControllerClass()
start = time.time()
timeOld = time.time()


while True:
    if firstLoop: firstLoop = False

    #Time set ups
    timeNow = time.time()
    beginTime = time.time() # moved from inside loop
    dt = timeNow - timeOld
    elapsedTime = np.round(beginTime - start, decimals=1)
    timeOld = timeNow


    ret, frame = cap.read()
    frame = imutils.resize(frame, width = adjustedWidth)
    # print(frame.shape[:2])

    measAngle, frame, gray, gray_blurred, frame_delta, erode, mask, transient_movement_flag = wd.loop(firstLoop,frame)
    if measAngle == None: measAngle = measAngleLast
    measAngleLast = measAngle

    _, _, measAngle = AngleXform(measAngle,fieldStart,horzEnd,fieldStart,vertEnd)

    # refAngle = controller.ref(elapsedTime)
    refAngle = 45
    ctrlAngle = controller.control(dt, elapsedTime, refAngle, measAngle)
    bus.write_byte(addr,int(ctrlAngle))

    # print("MEASURED ANGLE: ",measAngle)
    # print("REFERENCE ANGLE: ",refAngle)
    # print("CONTROL ANGLE: ",ctrlAngle)
    # print("ELAPSED TIME: ", elapsedTime)

    # Prepare frame with text space
    frame_with_text = np.zeros((frame_height, actual_frame_width, 3), dtype=np.uint8)
    frame_with_text[:actual_frame_height, :, :] = frame  # Only copy the video part, ensure dimensions match
    # print(frame_with_text.shape[:2])


    # Generate info text
    if ctrlAngle == None: ctrlAngle = -1
    info_text = f"MEASURED ANGLE: {measAngle:.2f}\nREFERENCE ANGLE: {refAngle:.2f}\nCONTROL ANGLE: {ctrlAngle:.2f}\nELAPSED TIME: {int(time.time() - start)} sec"

    # Display text on frame
    y0, dy = actual_frame_height + 30, 30  # Start text 10 pixels below the original frame
    for i, line in enumerate(info_text.split('\n')):
        y = y0 + i * dy
        cv.putText(frame_with_text, line, (10, y), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # annotate frame_annotated
    frame = cv.line(frame, fieldStart, horzEnd, color=(255,0,0), thickness=3) # horizontal edge
    frame = cv.line(frame, fieldStart, vertEnd, color=(0,255,0), thickness=3) # vertical edge

    # output

    # concatenate image Horizontally
    winTop = np.concatenate((frame, gray, gray_blurred), axis=1)
    winBot = np.concatenate((frame_delta, mask, erode), axis=1)
    # concatenate image Vertically
    winStack = np.concatenate((winTop, winBot), axis=0) 

    cv.imshow("Output Frame", frame_with_text) # measurements
    # cv.imshow("Output Frame", winStack) # 6-pane


    if outputFlag: result.write(frame_with_text)

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
