import numpy as np
import matplotlib.pyplot as plt

def maskPolyReg(mask):
    indices = np.where(mask == 255)
    if indices[0].size == 0 or indices[1].size == 0:
        print("No points found in the mask with the specified value.")
        return None, None, None, None

    x = indices[1]
    y = indices[0]

    # Fit a second-degree polynomial
    coefs = np.polynomial.polynomial.Polynomial.fit(x, y, 2).convert().coef
    print("Coefs: ", coefs)
    
    xPred = np.linspace(np.min(x), np.max(x), 100)
    yPred = coefs[0] + coefs[1]*xPred + coefs[2]*np.power(xPred, 2)
    yPred = yPred.astype(int)

    return x, y, xPred, yPred

# Create a simple mask with a quadratic distribution of points
mask = np.zeros((100, 100), dtype=np.uint8)
x = np.arange(10, 90)
y = 0.05 * (x - 50)**2 + 10  # Adjusted the scale and offset
y = y.astype(int)
mask[y, x] = 255

# Plot the mask to visualize it
plt.figure()
plt.imshow(mask, cmap='gray')
plt.title("Mask with Quadratic Points")
plt.show()

# Test the maskPolyReg function
x, y, xPred, yPred = maskPolyReg(mask)

# Plot the results
plt.figure()
plt.imshow(mask, cmap='gray')
plt.scatter(x, y, color='red', label='Original Points')
plt.plot(xPred, yPred, color='blue', label='Polynomial Fit')
plt.title("Polynomial Fit Result")
plt.legend()
plt.show()
