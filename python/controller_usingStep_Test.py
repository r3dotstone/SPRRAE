import numpy as np
import time
from controller import Controller

### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

start = time.time()
timeOld = time.time()

kp_omega = 0.01
ki_omega = 0.001

refAngle = 0 #deg

omega = 5 #[deg/s]
measuredAngle = 0 #need to figure out how we're getting this from the video
ei_omega = 0

while True:
    time.sleep(1)
    timeNow = time.time()
    beginTime = time.time()
    dt = np.floor(timeNow - timeOld)
    elapsedTime = np.floor(beginTime - start)
    timeOld = timeNow

    #controller
    e_omega = refAngle - measuredAngle #error between the angles
    ei_omega += e_omega * dt
    omega = 0.1 + kp_omega * e_omega + ki_omega * ei_omega 

    #Step
    if elapsedTime <= 2:
        refAngle = 0
    elif elapsedTime <=5:
        refAngle = 20
    else:
         refAngle = 70
    print("Time ", elapsedTime, "Step angle ", refAngle,"e omega ",e_omega, "e_i ", ei_omega)