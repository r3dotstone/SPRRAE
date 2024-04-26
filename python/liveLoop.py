import numpy as np
import time
from theController import theControllerClass

### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

controller = theControllerClass()
start = time.time()
timeOld = time.time()

while True:
    timeNow = time.time()
    beginTime = time.time()
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow
    controller.control()
