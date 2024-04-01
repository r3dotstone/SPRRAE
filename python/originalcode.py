# -*- coding: utf-8 -*-

import imutils
import cv2 as cv
import numpy as np
import os

# =============================================================================
# USER-SET PARAMETERS
# =============================================================================

# FILES
input_file = "stablePaintStreamCUT.avi"
output_file = "stablePaintStreamOUT.avi"
outputFlag = True

# mask lower threshold
MASK_THRESH = 20

# Number of frames to pass before changing the frame to compare the current
# frame against
FRAMES_TO_PERSIST = 10

# Minimum boxed area for a detected motion to count as actual motion
# Use to filter out noise or small objects
MIN_SIZE_FOR_MOVEMENT = 2000

# Minimum length of time where no motion is detected it should take
#(in program cycles) for the program to declare that there is no movement
MOVEMENT_DETECTED_PERSISTENCE = 100

# =============================================================================
# CORE PROGRAM
# =============================================================================

# Create capture and writer objects
cap = cv.VideoCapture(5) # Flush the stream
cap.release()

filePath = os.path.realpath(__file__)
fileDir = os.path.dirname(filePath)
vidDir = fileDir.replace('SPRRAE\python', 'vids')
input_path = os.path.join(vidDir,input_file)
output_path = os.path.join(vidDir,output_file)

cap = cv.VideoCapture(input_path)

if outputFlag:

    frame_width = 800 #int(cap.get(3)) 
    frame_height = 450 #int(cap.get(4)) 
    
    size = (frame_width, frame_height) 
    result = cv.VideoWriter(output_path, cv.VideoWriter_fourcc(*"MPEG"), 30, size)

# Init frame variables
first_frame = None
next_frame = None

# Init display font and timeout counters
font = cv.FONT_HERSHEY_SIMPLEX
delay_counter = 0
movement_persistent_counter = 0

# LOOP!
while True:

    # Set transient motion detected as false
    transient_movement_flag = False

    # Read frame
    ret, frame = cap.read()
    text = "Unoccupied"

    # If there's an error in capturing
    if not ret:
        print("CAPTURE ERROR")
        break

    # Resize and save a greyscale version of the image
    frame = imutils.resize(frame, width = 400)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Blur it to remove camera noise (reducing false positives)
    gray_blurred = cv.GaussianBlur(gray, (21, 21), 0)

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
    thresh = cv.threshold(frame_delta, 25, 255, cv.THRESH_BINARY)[1]

    # Fill in holes via dilate(), and find contours of the thesholds
    thresh = cv.dilate(thresh, None, iterations = 2)
    cnts, _ = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

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
    cv.putText(frame, str(text), (10,35), font, 0.75, (255,255,255), 2, cv.LINE_AA)

    # For if you want to show the individual video frames
#    cv.imshow("frame", frame)
#    cv.imshow("delta", frame_delta)

    # threshold mask
    _,mask = cv.threshold(frame_delta,MASK_THRESH,255,cv.THRESH_BINARY)

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

    cv.imshow("look! cool!", winStack)

    if outputFlag: 
        result.write(winStack)

    print(winStack.shape[1],winStack.shape[0])

    # Interrupt trigger by pressing q to quit the open CV program
    ch = cv.waitKey(1)
    if ch & 0xFF == ord('q'):
        break

# Cleanup when closed
cv.waitKey(0)
cv.destroyAllWindows()
cap.release()
result.release()
