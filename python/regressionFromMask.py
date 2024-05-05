import numpy as np
import matplotlib.pyplot as plt

def maskLinearReg(mask):
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

def maskPolyReg(mask):

    indices = np.where(mask == 255)
    
    # Check if the indices arrays are empty
    if indices[0].size == 0 or indices[1].size == 0:
        print("No points found in the mask with the specified value.")
        return None, None, None, None  # Adjust return values as per your requirement

    x = indices[1]
    y = indices[0]

    # Fit a second-degree polynomial
    coefs = np.polynomial.polynomial.Polynomial.fit(x, y, 2).convert().coef
    # print("coefs: ", coefs)
    
    # Prediction over the range of x
    xPred = np.linspace(np.min(x), np.max(x), 100)  # Using 100 points for prediction
    yPred = coefs[0] + coefs[1]*xPred + coefs[2]*np.power(xPred, 2)
    xPred = xPred.astype(int)
    yPred = yPred.astype(int)  # Convert to integers if required for further processing

    return indices[1], indices[0], xPred, yPred
    # indices = np.where(mask == 255) # stuff goes wrong if this returns nothing
    # # print("INDICES: ",indices)
    
    # # if indices == (np.array(None,dtype=np.int64), np.array(None,dtype=np.int64)): # checks if empty/no points were found
    # #     print("EMPTYYYYYYYYYY")
    # #     return #0, 0, np.array([0,mask.shape[1]]), np.array([0,0]),

    # # else:
    # x = indices[1]
    # y = indices[0]

    # coefs = np.polynomial.polynomial.Polynomial.fit(x, y, 2).coef
    # print("coefs: ", coefs)
    # xPred = x
    # yPred = coefs[0] + coefs[1]*x + coefs[2]*pow(x,2)

    # return indices[1], indices[0], xPred, yPred # need integers for cv.line!!