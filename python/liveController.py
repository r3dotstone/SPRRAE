import numpy as np
import time

### INPUT: position of stream from vision 
### OUTPUT: demand for position to i2c

# Parameters
rd = 25

kp = 0.2
ki = 1.4

kp_omega = 0.01
ki_omega = 0.001

dt = 0

sd = 2
M = 17
# Reference Signal

# Controller

a = 2 * 4 * 0.85
b = 16

ei = 0
e_old = 0
outd = np.zeros(loops)
out = np.zeros_like(outd)

omega = 0.1
output = np.zeros(loops)
angle = 0
ei_omega = 0

# if i >= 410:
j = i - 408
ydd = (M - 17) / (0.31 / 16) - a * outd[j - 1] - b * out[j - 1]
outd[j] = outd[j - 1] + ydd * dt
out[j] = out[j - 1] + outd[j] * dt

yp = out[j] + rd
if j > 1 / dt:
    out_delay = out[j - int(1 / dt)] + rd
else:
    out_delay = rd
dp = rd - out_delay

if i % 200 == 0:
    e = rd - (dp + yp)
    ei += e * dt
    ed = (e - e_old) / dt
    M += kp * e + ki * ei
    M = min(max(M, 12), 23)

speed = np.array([M, sd])

if i % 100 == 0:
    e_omega = 360 * (0.1 * dt * i) / (2 * np.pi) - angle
    ei_omega += e_omega * dt
    omega = 0.1 + kp_omega * e_omega + ki_omega * ei_omega

    output[i] = M

    om = 360 * omega * dt / (2 * np.pi)
    angle += om