import matplotlib.pyplot as plt
import imutils
import os
import cv2 as cv

input_file = "snapshot.png"
# output_file = "test.mp4"
filePath = os.path.realpath(__file__)
fileDir = os.path.dirname(filePath)
inDir = fileDir.replace('python', 'inputVids')
# outDir = fileDir.replace('python', 'outputVids')
input_path = os.path.join(inDir,input_file)
# output_path = os.path.join(outDir,output_file)

# img = plt.imread(input_path)

cap = cv.VideoCapture(0)
ret, img = cap.read()

adjustedWidth = 400
img = imutils.resize(img, width = adjustedWidth)
plt.imshow(img)
plt.show()