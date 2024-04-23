import numpy as np
import matplotlib.pyplot as plt
from fiat500PowerFunction import fiat500PowerFunction
from icePowerTorqueClass import icePowerTorqueClass

pf = fiat500PowerFunction()
icePT = icePowerTorqueClass()

rpmRange = np.arange(1500,5000,1)
powerOutput = np.array([])
trtlPos = 0.5

for rpmCurr in rpmRange:
    newPower = icePT.getSSPower(trtlPos,rpmCurr)
    powerOutput = np.append(powerOutput,newPower)

plt.figure("Test Power Plot")
plt.plot(rpmRange,powerOutput)
plt.xlabel("RPM")
plt.ylabel("Power")
plt.show()
