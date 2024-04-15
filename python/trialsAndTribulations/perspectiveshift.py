import cv2 as cv
import numpy as np
import imutils
import os

# https://pixspy.com/
inputFile = "stablePaintFrame.png"
outputFile = "stablePaintFrameOUT.png"
save = True

filePath = os.path.realpath(__file__)
fileDir = os.path.dirname(filePath)
imgDir = fileDir.replace('SPRRAE\python', 'pics')
inputPath = os.path.join(imgDir,inputFile)
print(inputPath)
img = cv.imread(inputPath)

# Coordinates that you want to Perspective Transform
startPts = np.float32([[120,70],[1013,67],[50,650],[1117,644]])
# Size of the Transformed Image
endPts = np.float32([[0,0],[1280,0],[0,720],[1280,720]])
# put some little circles on there
for val in startPts:
    cv.circle(img,(int(val[0]),int(val[1])),10,(0,0,255),-1)
# transformation matrix
M = cv.getPerspectiveTransform(startPts,endPts)
# transformed image
dst = cv.warpPerspective(img,M,(1280,720))
# before/after
cat = np.concatenate((img, dst), axis=1)
cat = imutils.resize(cat, width = 600)

#show results
cv.imshow("warp",cat)
cv.waitKey(0)
#stuff for saving
if save:
    cv.imwrite(os.path.join(imgDir,outputFile),cat)

# Closes all the frames
cv.destroyAllWindows()
