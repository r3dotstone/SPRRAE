#Zoe's attempt to turn Matlab controler into python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from matplotlib import animation


def distribution3(t, speed, launchAngleXY, windSpeed, shift):
    # Generate initial velocity from Gaussian distribution
    initialVelocity = np.random.normal(speed[0], speed[1])

    # Generate launch angle for horizontal and vertical motion
    angleZ = np.random.normal(23, 0)  # Assuming mean m = 23 and sd = 0 for angleZ
    xydev = np.random.normal(0, 0)  # Assuming mean m1 = 0 and sd1 = 0 for xydev

    # Constants
    gravity = 9.81  # Acceleration due to gravity (m/s^2)

    # Convert angles to radians
    launchAngleXYRad = np.deg2rad(launchAngleXY) + xydev
    launchAngleZRad = np.deg2rad(angleZ)

    # Extract wind speed components
    windspeedX = windSpeed[0]
    windspeedY = windSpeed[1]

    # Calculate components of initial velocity
    initialVelocityX = initialVelocity * np.cos(launchAngleXYRad) + windspeedX
    initialVelocityY = initialVelocity * np.sin(launchAngleXYRad) + windspeedY
    initialVelocityZ = initialVelocity * np.sin(launchAngleZRad)  # Update for vertical motion

    # Horizontal motion
    x = initialVelocityX * t
    y = initialVelocityY * t

    # Vertical motion
    z = initialVelocityZ * t - (0.5 * gravity * t ** 2)  # Update for vertical motion

    # Set negative z values to NaN (no data)
    z[z < 0] = np.nan

    # Shift the trajectory by 'shift' units
    x = np.roll(x, shift)
    x[:shift] = np.nan
    y = np.roll(y, shift)
    y[:shift] = np.nan
    z = np.roll(z, shift)
    z[:shift] = np.nan

    return x, y, z


# Parameters
feet2meter = 0.3048

cannons = np.array([[11, 0], [125, 0], [245, 0], [357, 0], [11, 234], [125, 234], [245, 234], [357, 234]])
can = cannons * feet2meter

loops = 3000
t_end = 10
dt = t_end / loops
t = np.arange(0.001, t_end, dt)
rot = 90 / t
disp_guess = 5

mod_const = loops / t_end / 30

sd = 2
m = 17
speed = np.array([m, sd])

windspeed = np.array([4, 0])

frame = np.zeros(t_end * 20, dtype=object)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x_min, x_max = 0, 2 * can[1, 0]
y_min, y_max = 0, 2 * can[1, 0]
num_points = 100  # Adjust as needed

# Generate the grid of points
x = np.linspace(x_min, x_max, num_points)
y = np.linspace(y_min, y_max, num_points)
X, Y = np.meshgrid(x, y)

# Compute the corresponding values of Z based on some function or data
Z = np.zeros_like(X)  # Initialize Z with zeros for now

# Plot the surface using X, Y, and Z
ax.plot_surface(X, Y, Z)

ax.set_zlim(-0.5, 5)

x = np.zeros((loops, loops))
y = np.zeros_like(x)
z = np.zeros_like(x)

remains = 30
xf = np.zeros(remains)
yf = np.zeros_like(xf)

xm = np.zeros(loops)
ym = np.zeros_like(xm)
xsd = np.zeros_like(xm)
ysd = np.zeros_like(xm)

rd = 25

kp = 0.2
ki = 1.4

kp_omega = 0.01
ki_omega = 0.001

a = 2 * 4 * 0.85
b = 16

M = m
ei = 0
e_old = 0
outd = np.zeros(loops)
out = np.zeros_like(outd)

omega = 0.1
output = np.zeros(loops)
angle = 0
ei_omega = 0

for i in range(loops):
    if i >= 410:
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

    [x[:, i], y[:, i], z[:, i]] = distribution3(t, speed, angle, windspeed, i-1)

    ax.plot_surface(X, Y, Z, color='#77AC30')
    ax.set_title(f"Mean Velocity = {M}")

    floor = np.where(z[:, i] == 0)[0]
    floor = floor[floor < i]
    in_floor = len(floor)
    if in_floor > 0:
        xf[:in_floor] = 0
        yf[:in_floor] = 0

    if len(floor) > 0:
        xf[:in_floor] = x[i, floor]
        yf[:in_floor] = y[i, floor]

    zf = np.zeros_like(xf)
    ax.scatter3D(xf, yf, zf, c='y')

    xm[i] = np.mean(xf)
    xsd[i] = np.std(xf)
    ym[i] = np.mean(yf)
    ysd[i] = np.std(yf)
    rd = np.sqrt(xm[i] ** 2 + ym[i] ** 2)
    theta = 360 * np.arctan2(ym[i], xm[i]) / (2 * np.pi)

    targetx = rd * np.cos(np.radians(angle))
    targety = rd * np.sin(np.radians(angle))

    ax.scatter3D(xm[i], ym[i], 8, c='r')
    ax.plot([xm[i] + xsd[i], xm[i] - xsd[i]], [ym[i], ym[i]], [8, 8], linewidth=2, c='r')
    ax.plot([xm[i], xm[i]], [ym[i] + ysd[i], ym[i] - ysd[i]], [8, 8], linewidth=2, c='r')
    ax.plot([targetx, targetx], [targety, targety], [8, 8], '*', markersize=10, c='m')

    ax.scatter3D(x[:, i], y[:, i], z[:, i], c='b')

    ax.set_xlim(0, 2 * can[1, 0])
    ax.set_ylim(0, 2 * can[1, 0])
    ax.set_zlim(-0.5, 8)

    # Set the elevation and azimuth angles to show the x-y plane
    ax.view_init(elev=90, azim=-90)
    plt.pause(0.001)
    ax.clear()


def update(frame):
    ax.clear()
    ax.plot_surface(X, Y, Z, color='#77AC30')
    ax.scatter3D(x[frame], y[frame], z[frame], c='b')
    ax.set_title(f"Frame {frame}")
    ax.set_xlim(0, 2 * can[1, 0])
    ax.set_ylim(0, 2 * can[1, 0])
    ax.set_zlim(-0.5, 8)


# Save animation
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
anim = FuncAnimation(fig, update, frames=np.arange(0, loops), interval=50)
anim.save('cannon_spray.mp4', writer=writer)

plt.show()
