# -*- coding: utf-8 -*-

import imutils
import cv2 as cv
import numpy as np
import os

# =============================================================================
# USER-SET PARAMETERS
# =============================================================================

# FILES
input_file = "DroneTop.avi"
output_file = "DroneTopOUT.mp4"
outputFlag = False
displayFlag = True

# movement lower threshold
MOV_THRESH = 12

# number of dilation/erosion iterations
DIL_ERODE_ITERS = 0

# mask lower threshold (change MOV_THRESH instead)
MASK_THRESH = 0

# Gaussian blue kernal size
BLUR_SIZE = 7

# Number of frames to pass before changing the frame to compare the current
# frame against
FRAMES_TO_PERSIST = 1

# Minimum boxed area for a detected motion to count as actual motion
# Use to filter out noise or small objects
MIN_SIZE_FOR_MOVEMENT = 1000

# Minimum length of time where no motion is detected it should take
#(in program cycles) for the program to declare that there is no movement
MOVEMENT_DETECTED_PERSISTENCE = 100

# =============================================================================
# CORE PROGRAM
# =============================================================================

filePath = os.path.realpath(__file__)
fileDir = os.path.dirname(filePath)
print("file dir: ",fileDir)
inDir = fileDir.replace('python', 'inputVids')
outDir = fileDir.replace('python', 'outputVids')
input_path = os.path.join(inDir,input_file)
output_path = os.path.join(outDir,output_file)
print("path: ",input_path)
cap = cv.VideoCapture(input_path)

if outputFlag:

    frame_width = 800 #int(cap.get(3)) 
    frame_height = 450 #int(cap.get(4)) 
    
    size = (frame_width, frame_height) 
    result = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*"mp4v"), 30, size)

# Init frame variables
first_frame = None
next_frame = None

# Init display font and timeout counters
font = cv.FONT_HERSHEY_SIMPLEX
delay_counter = 0
movement_persistent_counter = 0

firstLoop = True

# LOOP!
while True:

    # Set transient motion detected as false
    transient_movement_flag = False

    # Read frame
    ret, frame = cap.read()
    text = "Unoccupied"

    if not(ret) and firstLoop:
        print("CAPTURE ERROR")
        break
    if not ret:
        print("something cool probably happend")
        break

    # Resize and save a greyscale version of the image
    frame = imutils.resize(frame, width = 400)
    output = frame
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Apply edge detection method on the image
    edges = cv.Canny(gray, 130, 150, apertureSize=3)
    
    # This returns an array of r and theta values
    lines = cv.HoughLines(edges, 1, np.pi/180, 200)
    
    # The below for loop runs till r and theta values
    # are in the range of the 2d array
    r_theta = 0
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        # Stores the value of cos(theta) in a
        a = np.cos(theta)
    
        # Stores the value of sin(theta) in b
        b = np.sin(theta)
    
        # x0 stores the value rcos(theta)
        x0 = a*r
    
        # y0 stores the value rsin(theta)
        y0 = b*r
    
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta))
        x1 = int(x0 + 1000*(-b))
    
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta))
        y1 = int(y0 + 1000*(a))
    
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta))
        x2 = int(x0 - 1000*(-b))
    
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta))
        y2 = int(y0 - 1000*(a))
    
        # cv.line draws a line in img from the point(x1,y1) to (x2,y2).
        # (0,0,255) denotes the colour of the line to be
        # drawn. In this case, it is red.
        cv.line(output, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # convert to color for spplicing
    gray = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
    edges = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)

    # show frame
    # concatenate image Horizontally 
    winTop = np.concatenate((frame, gray), axis=1) 
    winBot = np.concatenate((edges, output), axis=1) 
    # concatenate image Vertically 
    winStack = np.concatenate((winTop, winBot), axis=0)  

    if displayFlag: cv.imshow("look! cool!", winStack)

    if outputFlag: result.write(winStack)

    # print(winStack.shape[1],winStack.shape[0])

    # Interrupt trigger by pressing q to quit the open CV program
    ch = cv.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

    if firstLoop: firstLoop = False


# Cleanup when closed
cv.waitKey(0)
cv.destroyAllWindows()
cap.release()
if outputFlag: result.release()
