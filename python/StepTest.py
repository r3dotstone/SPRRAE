import numpy as np
import time
from controller import Controller

### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

start = time.time()
timeOld = time.time()
rotVelocity = 3 #[deg/s]
period = 30 #[s]
refAngle = 0 #deg
direction = 1

while True:
    time.sleep(1)
    timeNow = time.time()
    beginTime = time.time()
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow

    if elapsedTime < 5:
        refAngle = 20
    else:
        refAngle = 70
    print("angle ", refAngle, "elapsed time", elapsedTime)