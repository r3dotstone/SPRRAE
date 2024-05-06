# -*- coding: utf-8 -*-

import imutils
import cv2 as cv
import numpy as np
import os
from regressionFromMask import maskPolyReg

class waterDetector:

    def __init__(self):


        # movement lower threshold
        self.MOV_THRESH = 2

        # number of dilation/erosion iterations
        self.DIL_ERODE_ITERS = 3 # CHANGE

        # mask lower threshold (change MOV_THRESH instead)
        self.MASK_THRESH = 0

        # Gaussian blue kernal size
        self.BLUR_SIZE = 11 # CHANGED from 7 to 9 to 11

        # Number of frames to pass before changing the frame to compare the current
        # frame against
        self.FRAMES_TO_PERSIST = 1

        # Minimum boxed area for a detected motion to count as actual motion
        # Use to filter out noise or small objects
        self.MIN_SIZE_FOR_MOVEMENT = 200 # CHANGED from 100 to 200

        # Minimum length of time where no motion is detected it should take
        #(in program cycles) for the program to declare that there is no movement
        # self.MOVEMENT_DETECTED_PERSISTENCE = 100

        # Init frame variables
        self.first_frame = None
        self.next_frame = None

        # Init display font and timeout counters
        self.font = cv.FONT_HERSHEY_SIMPLEX
        self.delay_counter = 0
        self.movement_persistent_counter = 0

    def loop(self, firstLoop, frame):

        # Set transient motion detected as false
        transient_movement_flag = False

        # Resize and save a greyscale version of the image
        # frame = imutils.resize(frame, width = 200)
        # print("size: ",frame.shape)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Blur it to remove camera noise (reducing false positives)
        gray_blurred = cv.GaussianBlur(gray, (self.BLUR_SIZE, self.BLUR_SIZE), 0)

        # If the first frame is nothing, initialise it
        if self.first_frame is None: self.first_frame = gray_blurred

        self.delay_counter += 1

        # Otherwise, set the first frame to compare as the previous frame
        # But only if the counter reaches the appriopriate value
        # The delay is to allow relatively slow motions to be counted as large
        # motions if they're spread out far enough
        if self.delay_counter > self.FRAMES_TO_PERSIST:
            self.delay_counter = 0
            self.first_frame = self.next_frame


        # Set the next frame to compare (the current frame)
        self.next_frame = gray_blurred

        # Compare the two frames, find the difference
        frame_delta = cv.absdiff(self.first_frame, self.next_frame)
        thresh = cv.threshold(frame_delta, self.MOV_THRESH, 255, cv.THRESH_BINARY)[1]

        # Fill in holes via dilate(), and find contours of the thesholds
        dil = cv.dilate(thresh, None, iterations = self.DIL_ERODE_ITERS)
        erode = cv.erode(dil,None, iterations = self.DIL_ERODE_ITERS)
        cnts, _ = cv.findContours(erode.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:

            # If the contour is too small, ignore it, otherwise, there's transient
            # movement
            if cv.contourArea(c) > self.MIN_SIZE_FOR_MOVEMENT:
                transient_movement_flag = True

        # The moment something moves momentarily, reset the persistent
        # movement timer.
        if transient_movement_flag == True:
            self.movement_persistent_flag = True
            # self.movement_persistent_counter = self.MOVEMENT_DETECTED_PERSISTENCE

        # threshold mask
        _,mask = cv.threshold(erode,self.MASK_THRESH,255,cv.THRESH_BINARY)

        angle = None # when no movement detect/no data
        frame_annotated = frame
        if not(firstLoop) and transient_movement_flag:
            _, _, xPred, yPred = maskPolyReg(mask)
            for i in np.linspace(0,len(xPred)-1,25,dtype=int):
                # j = 20 % i
                circleCoord = (xPred[i],yPred[i])
                # if j == 0:
                frame_annotated = cv.circle(frame, circleCoord, radius=2, color=(127, 0, 127), thickness=-1)
            lineStart = (xPred[0],yPred[0])
            lineEnd = (xPred[-1],yPred[-1])
            color = (0, 0, 255)
            thickness = 3
            frame_annotated = cv.line(frame_annotated, lineStart, lineEnd, color, thickness)
            angle = np.rad2deg(np.arctan((lineEnd[1]-lineStart[1])/(lineEnd[0]-lineStart[0])))
            # cv.putText(frame, str(angle), (10,35), self.font, 0.75, (255,255,255), 2, cv.LINE_AA)

        # Convert to color for splicing
        gray = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)
        gray_blurred = cv.cvtColor(gray_blurred, cv.COLOR_GRAY2BGR)
        frame_delta = cv.cvtColor(frame_delta, cv.COLOR_GRAY2BGR)
        erode = cv.cvtColor(erode, cv.COLOR_GRAY2BGR)
        thresh = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)

        return angle, frame, gray, gray_blurred, frame_delta, erode, thresh, transient_movement_flag
