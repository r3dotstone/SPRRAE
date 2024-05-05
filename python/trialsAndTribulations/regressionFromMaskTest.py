from regressionFromMask import maskReg
import numpy as np
import matplotlib.pyplot as plt

mask = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                 [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
                 [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

pointsX, pointsY, x, y = maskReg(mask)

print(x,y)

plt.figure("Test")
plt.scatter(pointsX,pointsY)
plt.plot(x,y)
plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
#
# #                 V (0,0) Down is up
# # mask = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
# #                  [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
# #                  [0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
# #                  [0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
# #                  [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
# #                  [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
# #                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# #                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
# mask = np.load("regressionTestArray.npy")
#
#
# indices = np.where(mask == 255)
#
# x = indices[1]
# y = indices[0]
#
# # y = m*x + b
# # y = [xs ,ones] * [[m],
# #                   [b]]
#
# G = np.vstack((x,np.ones(x.shape))).T
# mb, _, _, _ = np.linalg.lstsq(G,y)
#
# xPred = np.array([np.min(x),np.max(x)])
# GPred = np.vstack((xPred,np.ones(xPred.shape))).T
# yPred = np.dot(GPred,mb)
#
# print("mb: ",mb,"xPred: ",xPred,"yPred: ",yPred)
#
#
# plt.figure("Test")
# plt.scatter(x,y)
# plt.plot(xPred,yPred)
# plt.show()
