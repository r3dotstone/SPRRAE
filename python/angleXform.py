import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os


def AngleXform(angle,horzStart,horzEnd,vertStart,vertEnd):
    mHorz = (horzEnd[1] - horzStart[1]) / (horzEnd[0] - horzStart[0])
    mVert = (vertEnd[1] - vertStart[1]) / (vertEnd[0] - vertStart[0])
    m = np.tan(angle)
   
    angleHorzToVert = np.arctan((mVert-mHorz)/(1+(mHorz*mVert)))
    scale = angleHorzToVert/(np.pi/2)

    angleToHorz = angle - np.arctan(mHorz)
    angleScaled = scale * angleToHorz

    return angleHorzToVert, angleToHorz, angleScaled