#Zoe's attempt to turn Matlab controler into python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

feet2meter = 0.3048

cannons = np.array([[11, 0], [125, 0], [245, 0], [357, 0], [11, 234], [125, 234], [245, 234], [357, 234]])
can = cannons * feet2meter

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

X = np.array([0, 2 * can[1, 0], 2 * can[1, 0], 0])
Y = np.array([0, 0, 2 * can[1, 0], 2 * can[1, 0]])
Z = np.zeros_like(X)

ax.plot_surface(X, Y, Z)

ax.set_zlim(-0.5, 5)

loops = 3000
t_end = 10
dt = t_end / loops
t = np.arange(0, t_end, dt)
rot = 90 / t
disp_guess = 5

mod_const = loops / t_end / 30

sd = 2
m = 17
N = loops
speed = np.array([m, sd])

windspeed = np.array([4, 0])

frame = np.zeros(t_end * 20, dtype=object)

x = np.zeros((loops, N))
y = np.zeros_like(x)
z = np.zeros_like(x)

x2 = np.zeros_like(x)
y2 = np.zeros_like(x)
z2 = np.zeros_like(x)

x3 = np.zeros_like(x)
y3 = np.zeros_like(x)
z3 = np.zeros_like(x)

x4 = np.zeros_like(x)
y4 = np.zeros_like(x)
z4 = np.zeros_like(x)

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

        yp = out[j] + r[409]
        if j > 1 / dt:
            out_delay = out[j - int(1 / dt)] + r[409]
        else:
            out_delay = r[409]
        dp = r[i - 1] - out_delay

        if i % 200 == 0:
            e = rd - (dp + yp)
            ei += e * dt
            ed = (e - e_old) / dt
            M += kp * e + ki * ei
            M = min(max(M, 12), 23)

        speed = np.array([M, sd])

        if i % 100 == 0:
            e_omega = target - theta
            ei_omega += e_omega * dt
            omega = 0.1 + kp_omega * e_omega + ki_omega * ei_omega

    output[i] = M

    om = 360 * omega * dt / (2 * np.pi)
    angle += om

    target = 360 * (0.1 * dt * i) / (2 * np.pi)

    x[i], y[i], z[i] = distribution3(t, speed, angle, windspeed, i - 1)
    ax.plot_surface(X, Y, Z, color='#77AC30')
    ax.set_title(f"Mean Velocity = {M}")

    floor = np.where(z[i] == 0)[0]
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
    r = np.sqrt(xm[i] ** 2 + ym[i] ** 2)
    theta = 360 * np.arctan2(ym[i], xm[i]) / (2 * np.pi)

    targetx = rd * np.cos(np.radians(target))
    targety = rd * np.sin(np.radians(target))

    ax.scatter3D(xm[i], ym[i], 8, c='r')
    ax.plot([xm[i] + xsd[i], xm[i] - xsd[i]], [ym[i], ym[i]], [8, 8], linewidth=2, c='r')
    ax.plot([xm[i], xm[i]], [ym[i] + ysd[i], ym[i] - ysd[i]], [8, 8], linewidth=2, c='r')
    ax.plot([targetx, targetx], [targety, targety], [8, 8], '*', markersize=10, c='m')

    ax.scatter3D(x[i], y[i], z[i], c='b')

    ax.set_xlim(0, 2 * can[1, 0])
    ax.set_ylim(0, 2 * can[1, 0])
    ax.set_zlim(-0.5, 8)

    plt.pause(0.001)
    ax.clear()

plt.show()

# Save animation
# anim = FuncAnimation(fig, update, frames=np.arange(0, t_end, dt), interval=50)
# anim.save('cannon_Spray6[mean].avi', writer='ffmpeg', fps=30)
