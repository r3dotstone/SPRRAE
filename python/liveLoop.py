import numpy as np
import time
from controller import Controller

### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

asdf = Controller()
start = time.time()
timeOld = time.time()

while True:
    timeNow = time.time()
    beginTime = time.time()
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow
    asdf.ref()
