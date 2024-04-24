import numpy as np
import matplotlib.pyplot as plt

def maskReg(mask):
    indices = np.where(mask == 255) # stuff goes wrong if this returns nothing
    # print("INDICES: ",indices)
    
    # if indices == (np.array(None,dtype=np.int64), np.array(None,dtype=np.int64)): # checks if empty/no points were found
    #     print("EMPTYYYYYYYYYY")
    #     return #0, 0, np.array([0,mask.shape[1]]), np.array([0,0]),

    # else:
    x = indices[1]
    y = indices[0]

    # y = m*x + b
    # y = [xs ,ones] * [[m],
    #                   [b]]

    G = np.vstack((x,np.ones(x.shape))).T
    mb, _, _, _ = np.linalg.lstsq(G,y)

    # xPred = x
    # if xPred.any() == None:
    #     pass
    xPred = np.array([np.min(x),np.max(x)])
    GPred = np.vstack((xPred,np.ones(xPred.shape))).T
    yPred = np.dot(GPred,mb)
    return indices[1], indices[0], xPred, yPred # need integers for cv.line!!
