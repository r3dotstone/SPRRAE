import cv2 as cv

inputFile = "stablePaintFrame.jpg"
outputFile = "stablePaintFrameOUT.jpg"
save = False

filePath = os.path.realpath(__file__)
fileDir = os.path.dirname(filePath)
imgDir = fileDir.replace('SPRRAE\python', 'pics')
input_path = os.path.join(imgDir,inputFile)
img = cv2.imread(inputFile)

# Coordinates that you want to Perspective Transform
startPts = np.float32([[219,209],[612,8],[380,493],[785,271]])
# Size of the Transformed Image
endPts = np.float32([[0,0],[500,0],[0,400],[500,400]])
# put some little circles on there
for val in startPts:
    cv.circle(img,(val[0],val[1]),5,(0,255,0),-1)
# transformation matrix
M = cv.getPerspectiveTransform(startPts,endPts)
# transformed image
dst = cv.warpPerspective(img,M,(500,400))
# before/after
cat = np.concatenate((img, dst), axis=1)
#show results
cv.imshow(cat)

#stuff for saving
if save:
    cv.imwrite(outputFile,cat)

# Closes all the frames
cv.destroyAllWindows()
