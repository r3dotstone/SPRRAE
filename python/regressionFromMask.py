import numpy as np
import matplotlib.pyplot as plt

def maskReg(mask):
    indices = np.where(mask == 1)

    x = indices[1]
    y = indices[0]

    # y = m*x + b
    # y = [xs ,ones] * [[m],
    #                   [b]]

    G = np.vstack((x,np.ones(x.shape))).T
    mb, _, _, _ = np.linalg.lstsq(G,y)

    xPred = np.array([np.min(x),np.max(x)])
    GPred = np.vstack((xPred,np.ones(xPred.shape))).T
    yPred = np.dot(GPred,mb)
    return indices[1], indices[0], xPred, yPred
