# -*- coding: utf-8 -*-

import imutils
import cv2 as cv
import numpy as np
import os
from regressionFromMask import maskReg

# =============================================================================
# USER-SET PARAMETERS
# =============================================================================

# FILES
input_file = "angleTest.avi"
output_file = "angleTestOUT.mp4"
outputFlag = False
displayFlag = True

# movement lower threshold
MOV_THRESH = 4

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
inDir = fileDir.replace('python', 'inputVids')
outDir = fileDir.replace('python', 'outputVids')
input_path = os.path.join(inDir,input_file)
output_path = os.path.join(outDir,output_file)

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
    frame = imutils.resize(frame, width = 200)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Blur it to remove camera noise (reducing false positives)
    gray_blurred = cv.GaussianBlur(gray, (BLUR_SIZE, BLUR_SIZE), 0)

    # If the first frame is nothing, initialise it
    if first_frame is None: first_frame = gray_blurred

    delay_counter += 1

    # Otherwise, set the first frame to compare as the previous frame
    # But only if the counter reaches the appriopriate value
    # The delay is to allow relatively slow motions to be counted as large
    # motions if they're spread out far enough
    if delay_counter > FRAMES_TO_PERSIST:
        delay_counter = 0
        first_frame = next_frame


    # Set the next frame to compare (the current frame)
    next_frame = gray_blurred

    # Compare the two frames, find the difference
    frame_delta = cv.absdiff(first_frame, next_frame)
    thresh = cv.threshold(frame_delta, MOV_THRESH, 255, cv.THRESH_BINARY)[1]

    # Fill in holes via dilate(), and find contours of the thesholds
    dil = cv.dilate(thresh, None, iterations = DIL_ERODE_ITERS)
    erode = cv.erode(dil,None, iterations = DIL_ERODE_ITERS)
    cnts, _ = cv.findContours(erode.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:

        # # Save the coordinates of all found contours
        # (x, y, w, h) = cv.boundingRect(c)

        # If the contour is too small, ignore it, otherwise, there's transient
        # movement
        if cv.contourArea(c) > MIN_SIZE_FOR_MOVEMENT:
            transient_movement_flag = True

            # # Draw a rectangle around big enough movements
            # cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # The moment something moves momentarily, reset the persistent
    # movement timer.
    if transient_movement_flag == True:
        movement_persistent_flag = True
        movement_persistent_counter = MOVEMENT_DETECTED_PERSISTENCE

    # As long as there was a recent transient movement, say a movement
    # was detected
    if movement_persistent_counter > 0:
        text = "Movement Detected " + str(movement_persistent_counter)
        movement_persistent_counter -= 1
    else:
        text = "No Movement Detected"

    # Print the text on the screen, and display the raw and processed video
    # feeds
    # cv.putText(frame, str(text), (10,35), font, 0.75, (255,255,255), 2, cv.LINE_AA)

    # For if you want to show the individual video frames
#    cv.imshow("frame", frame)
#    cv.imshow("delta", frame_delta)

    # threshold mask
    _,mask = cv.threshold(erode,MASK_THRESH,255,cv.THRESH_BINARY)
    pointsX, pointsY, lineX, lineY = maskReg(mask)
    lineStart = (lineX[0],lineY[0])
    lineEnd = (lineX[1],line[1])
    color = (0, 255, 0)
    thickness = 3
    frame = cv.line(frame, lineStart, lineEnd, color, thickness)


    # np.save("regressionTestArray",mask)

    # Convert to color for splicing
    gray_blurred = cv.cvtColor(gray_blurred, cv.COLOR_GRAY2BGR)
    frame_delta = cv.cvtColor(frame_delta, cv.COLOR_GRAY2BGR)
    mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

    # show frame
    # concatenate image Horizontally
    winTop = np.concatenate((frame, gray_blurred), axis=1)
    winBot = np.concatenate((frame_delta, mask), axis=1)
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
