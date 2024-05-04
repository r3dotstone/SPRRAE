import numpy as np
import time

class theControllerClass:
    def __init__(self):
        self.kp_omega = 0.1
        self.ki_omega = 0.01
        #self.dt = 0 #[milliseconds] <------PROBLEM???
        self.angle = 0
        self.ei_omega = 0
        self.omega = 0.1 #[deg/s]

    def control(self, dt, elapsedTime, refAngle, measuredAngle):
        # #measuredAngle = 0 #need to figure out how we're getting this from the video

        if (elapsedTime % 1) == 0: self.angle = 0
        e_omega = refAngle - measuredAngle #error between the angles
        self.ei_omega += e_omega * dt
        omega = 0.1 + self.kp_omega * e_omega + self.ki_omega * self.ei_omega # 0.1 PROMBLEM???
        # # print(omega)
        # # time.sleep(0.3) #delay 1/3 second <------PROBLEM???
        dAngle = omega * dt
        self.angle += dAngle
        #self.angle = omega
        return self.angle

    def ref(self, elapsedTime): #WORKING!!!!
         #step function velocity vs time
         #the period is 60s for 180 deg rotation
        rotVelocity = 3 #[deg/s]
        period = 30 #[s] for 90 degrees, 60 seconds for 180 degerees
        refAngle = 0
        direction = 1

         #What needs to be looped in while True loop
        refAngle += (rotVelocity * elapsedTime * direction)
        if elapsedTime % period == 0:
            direction = -1*direction
        return refAngle

    def stepTests(self, elapsedTime):
        if elapsedTime < 5:
            refAngle = 20
        else:
            refAngle = 70
        print(refAngle)
